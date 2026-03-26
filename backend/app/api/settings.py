from fastapi import APIRouter
from sqlalchemy import select
from app.dependencies import DbSession, RequiredUserId
from app.models.user_settings import UserSettings
from app.utils.crypto import encrypt_api_key, decrypt_api_key
from app.ai.llm.base import LLMConfig
from app.ai.llm.factory import create_llm

router = APIRouter()


@router.get("")
async def get_settings(db: DbSession, user_id: RequiredUserId):
    """获取用户 BYOK 设置（API Key 脱敏返回）"""
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == user_id))
    s = result.scalar_one_or_none()
    if not s:
        return {"code": 200, "msg": "success", "data": None}
    return {
        "code": 200,
        "msg": "success",
        "data": {
            "llm_base_url": s.llm_base_url,
            "llm_model_name": s.llm_model_name,
            "llm_api_key_set": bool(s.llm_api_key_enc),  # 只告知是否已设置，不返回明文
            "preferred_categories": s.preferred_categories,
            "language": s.language,
            "daily_digest": s.daily_digest,
        },
    }


@router.put("")
async def update_settings(body: dict, db: DbSession, user_id: RequiredUserId):
    """更新 BYOK 设置，API Key 落库前加密"""
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == user_id))
    s = result.scalar_one_or_none()

    if not s:
        s = UserSettings(user_id=user_id)
        db.add(s)

    if "llm_base_url" in body:
        s.llm_base_url = body["llm_base_url"]
    if "llm_model_name" in body:
        s.llm_model_name = body["llm_model_name"]
    if "llm_api_key" in body and body["llm_api_key"]:
        s.llm_api_key_enc = encrypt_api_key(body["llm_api_key"])
    if "preferred_categories" in body:
        s.preferred_categories = body["preferred_categories"]
    if "language" in body:
        s.language = body["language"]
    if "daily_digest" in body:
        s.daily_digest = body["daily_digest"]

    await db.commit()
    return {"code": 200, "msg": "设置已保存", "data": None}


@router.post("/test-llm")
async def test_llm(db: DbSession, user_id: RequiredUserId):
    """测试用户 BYOK LLM 连通性"""
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == user_id))
    s = result.scalar_one_or_none()
    if not s or not s.llm_api_key_enc:
        return {"code": 400, "msg": "尚未配置 API Key", "data": None}

    try:
        api_key = decrypt_api_key(s.llm_api_key_enc)
        config = LLMConfig(
            base_url=s.llm_base_url or "https://api.openai.com/v1",
            api_key=api_key,
            model_name=s.llm_model_name or "gpt-4o-mini",
            max_tokens=10,
        )
        llm = create_llm(config)
        from openai import AsyncOpenAI
        client = AsyncOpenAI(base_url=config.base_url, api_key=config.api_key)
        await client.chat.completions.create(
            model=config.model_name,
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5,
        )
        return {"code": 200, "msg": "连接成功", "data": {"model": config.model_name}}
    except Exception as e:
        return {"code": 400, "msg": f"连接失败: {str(e)}", "data": None}
