from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from sqlalchemy import select, update
from app.dependencies import DbSession, CurrentUserId
from app.models.paper import Paper
from app.models.user_settings import UserSettings
from app.ai.llm.base import LLMConfig
from app.ai.llm.factory import create_llm, create_official_llm
from app.ai.summarizer import PaperSummarizer
from app.utils.crypto import decrypt_api_key
import json

router = APIRouter()


@router.get("/summarize/{paper_id}/stream")
async def summarize_stream(paper_id: str, db: DbSession, user_id: CurrentUserId):
    """SSE 流式生成摘要。
    - 已登录且有 BYOK 配置：使用用户自己的 LLM
    - 否则：使用系统官方额度
    """
    result = await db.execute(select(Paper).where(Paper.id == paper_id))
    paper = result.scalar_one_or_none()
    if not paper:
        return {"code": 404, "msg": "论文不存在", "data": None}

    # 已有摘要直接流式返回
    if paper.has_summary() and paper.summary_what:
        async def cached_stream():
            yield f"data: {json.dumps({'section': 'summary', 'delta': paper.summary_what}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(cached_stream(), media_type="text/event-stream")

    # 选择 LLM
    llm = await _get_user_llm(db, user_id) or create_official_llm()
    if not llm:
        return {"code": 400, "msg": "LLM 未配置", "data": None}

    summarizer = PaperSummarizer(llm)

    # 标记为 processing
    await db.execute(update(Paper).where(Paper.id == paper_id).values(summary_status="processing"))
    await db.commit()

    async def generate():
        parts: list[str] = []
        try:
            async for section, delta in summarizer.stream(paper.title, paper.abstract):
                parts.append(delta)
                yield f"data: {json.dumps({'section': 'summary', 'delta': delta}, ensure_ascii=False)}\n\n"

            # 写入数据库 - 使用 summary_what 存储摘要内容
            full_summary = "".join(parts)
            await db.execute(
                update(Paper).where(Paper.id == paper_id).values(
                    summary_what=full_summary,
                    summary_how=None,
                    summary_why=None,
                    summary_status="done",
                    summary_model=llm.config.model_name,
                )
            )
            await db.commit()
        except Exception as e:
            await db.execute(update(Paper).where(Paper.id == paper_id).values(summary_status="failed"))
            await db.commit()
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/summarize/{paper_id}/status")
async def summarize_status(paper_id: str, db: DbSession):
    """查询摘要生成状态"""
    result = await db.execute(select(Paper.summary_status).where(Paper.id == paper_id))
    status = result.scalar_one_or_none()
    if status is None:
        return {"code": 404, "msg": "论文不存在", "data": None}
    return {"code": 200, "msg": "success", "data": {"status": status}}


async def _get_user_llm(db: DbSession, user_id):
    """尝试获取用户 BYOK LLM 配置，失败返回 None"""
    if not user_id:
        return None
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == user_id))
    s = result.scalar_one_or_none()
    if not s or not s.llm_api_key_enc:
        return None
    try:
        api_key = decrypt_api_key(s.llm_api_key_enc)
        config = LLMConfig(
            base_url=s.llm_base_url or "https://api.openai.com/v1",
            api_key=api_key,
            model_name=s.llm_model_name or "gpt-4o-mini",
        )
        return create_llm(config)
    except Exception:
        return None
