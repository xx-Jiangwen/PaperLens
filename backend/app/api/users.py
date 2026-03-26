from fastapi import APIRouter
from sqlalchemy import select
from app.dependencies import DbSession, RequiredUserId
from app.models.user import User

router = APIRouter()


@router.get("/me")
async def get_me(db: DbSession, user_id: RequiredUserId):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return {"code": 404, "msg": "用户不存在", "data": None}
    return {
        "code": 200,
        "msg": "success",
        "data": {"id": user.id, "nickname": user.nickname, "avatar_url": user.avatar_url},
    }
