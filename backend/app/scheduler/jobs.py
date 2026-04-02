import logging
from app.sources import ALL_SOURCES
from app.config import settings

logger = logging.getLogger(__name__)


async def daily_fetch_papers():
    """每日定时抓取任务（每天 00:30 UTC，对应北京时间 08:30）。

    遍历所有已注册的数据源，抓取当日论文，upsert 到数据库。
    新论文 summary_status 默认为 pending，等待 summarize_pending_papers() 处理。
    """
    from app.db import AsyncSessionLocal
    from app.models.paper import Paper
    from sqlalchemy.dialects.sqlite import insert as sqlite_insert

    logger.info("开始每日论文抓取任务")
    total_new = 0

    for source in ALL_SOURCES:
        try:
            papers = await source.fetch_daily(
                categories=settings.daily_categories_list,
                max_per_category=settings.DAILY_MAX_PER_CATEGORY,
            )
            async with AsyncSessionLocal() as db:
                for p in papers:
                    # upsert：以 arxiv_id_base 为去重键
                    stmt = sqlite_insert(Paper).values(
                        id=p.id,
                        arxiv_id_base=p.arxiv_id_base,
                        title=p.title,
                        authors=p.authors,
                        abstract=p.abstract,
                        published_at=p.published_at,
                        updated_at=p.updated_at,
                        url=p.url,
                        pdf_url=p.pdf_url,
                        categories=p.categories,
                        primary_category=p.primary_category,
                        comment=p.comment,
                        journal_ref=p.journal_ref,
                        doi=p.doi,
                        source_name=p.source_name,
                    ).on_conflict_do_nothing(index_elements=["id"])
                    result = await db.execute(stmt)
                    total_new += result.rowcount
                await db.commit()

            logger.info(f"[{source.source_name}] 抓取 {len(papers)} 篇，新入库 {total_new} 篇")
        except Exception as e:
            logger.error(f"[{source.source_name}] 抓取失败: {e}", exc_info=True)

    logger.info(f"每日抓取完成，共新入库 {total_new} 篇")

    # 抓取完成后触发推送任务
    if total_new > 0:
        await push_daily_papers_notification(new_count=total_new)


async def summarize_pending_papers():
    """批量处理 pending 状态论文（每小时执行）。
    使用系统官方额度，每次处理最多 10 篇，避免额度超限。
    """
    from app.db import AsyncSessionLocal
    from app.models.paper import Paper
    from app.ai.llm.factory import create_official_llm
    from app.ai.summarizer import PaperSummarizer
    from sqlalchemy import select, update

    logger.info("开始批量摘要任务")
    llm = create_official_llm()
    summarizer = PaperSummarizer(llm)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Paper).where(Paper.summary_status == "pending").limit(10)
        )
        pending = result.scalars().all()

        for paper in pending:
            try:
                await db.execute(
                    update(Paper).where(Paper.id == paper.id).values(summary_status="processing")
                )
                await db.commit()

                summary = await summarizer.generate(paper.title, paper.abstract)

                await db.execute(
                    update(Paper).where(Paper.id == paper.id).values(
                        summary_what=summary.content,
                        summary_how=None,
                        summary_why=None,
                        summary_status="done",
                        summary_model=summary.model_used,
                    )
                )
                await db.commit()
                logger.info(f"摘要生成完成: {paper.id}")
            except Exception as e:
                await db.execute(
                    update(Paper).where(Paper.id == paper.id).values(summary_status="failed")
                )
                await db.commit()
                logger.error(f"摘要生成失败 {paper.id}: {e}")


async def push_daily_papers_notification(new_count: int = 0):
    """推送每日论文更新通知给订阅用户。

    在每日抓取完成后执行，向有推送配额的用户发送订阅消息。
    """
    from app.db import AsyncSessionLocal
    from app.models.user_subscription import UserSubscription
    from app.models.user import User
    from app.services.wechat_push import push_service
    from sqlalchemy import select, update
    from datetime import datetime, timezone

    logger.info("开始推送每日论文通知")

    # 消息模板ID（需要在微信公众平台申请）
    template_id = settings.WX_SUBSCRIBE_TEMPLATE_ID
    if not template_id:
        logger.warning("未配置订阅消息模板ID，跳过推送")
        return

    async with AsyncSessionLocal() as db:
        # 查询有配额且启用订阅的用户
        result = await db.execute(
            select(UserSubscription, User)
            .join(User, UserSubscription.user_id == User.id)
            .where(UserSubscription.enabled == True)
            .where(UserSubscription.push_quota > 0)
        )
        subscribers = result.all()

        if not subscribers:
            logger.info("没有待推送的订阅用户")
            return

        success_count = 0
        for sub, user in subscribers:
            try:
                # 发送订阅消息
                # 模板数据格式需要根据实际模板调整
                data = {
                    "thing1": {"value": f"今日新论文 {new_count} 篇"},
                    "time2": {"value": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")},
                    "thing3": {"value": "点击查看今日推荐"},
                }

                success = await push_service.send_subscribe_message(
                    openid=user.openid,
                    template_id=template_id,
                    data=data,
                    page="pages/home/index",
                )

                if success:
                    # 减少配额，更新推送时间
                    sub.push_quota -= 1
                    sub.last_pushed_at = datetime.now(timezone.utc)
                    success_count += 1
                else:
                    logger.warning(f"推送失败: user_id={user.id}")

            except Exception as e:
                logger.error(f"推送异常: user_id={user.id}, error={e}")

        await db.commit()

    logger.info(f"推送完成: 成功 {success_count}/{len(subscribers)}")
