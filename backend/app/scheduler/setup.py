from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.scheduler.jobs import daily_fetch_papers, summarize_pending_papers


def start_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    # 每天 00:30 UTC（北京时间 08:30）抓取当日论文
    scheduler.add_job(
        daily_fetch_papers,
        CronTrigger(hour=0, minute=30),
        id="daily_fetch",
        replace_existing=True,
    )

    # 每小时处理 pending 摘要
    scheduler.add_job(
        summarize_pending_papers,
        CronTrigger(minute=15),  # 每小时 15 分执行
        id="summarize_pending",
        replace_existing=True,
    )

    scheduler.start()
    return scheduler
