from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select, func
from app.dependencies import DbSession, RequiredUserId
from app.models.user import User
from app.models.bookmark import Bookmark
from datetime import datetime, timedelta, timezone

router = APIRouter()


class UpdateUserBody(BaseModel):
    nickname: str | None = None
    avatar_url: str | None = None


@router.get("/me")
async def get_me(db: DbSession, user_id: RequiredUserId):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return {"code": 404, "msg": "用户不存在", "data": None}
    return {
        "code": 200,
        "msg": "success",
        "data": {"id": user.id, "nickname": user.nickname or "PaperLens 用户", "avatar_url": user.avatar_url},
    }


@router.put("/me")
async def update_me(body: UpdateUserBody, db: DbSession, user_id: RequiredUserId):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return {"code": 404, "msg": "用户不存在", "data": None}
    if body.nickname is not None:
        nickname = body.nickname.strip()
        if not nickname or len(nickname) > 20:
            return {"code": 400, "msg": "昵称长度需在 1-20 个字符之间", "data": None}
        user.nickname = nickname
    if body.avatar_url is not None:
        user.avatar_url = body.avatar_url
    await db.commit()
    return {
        "code": 200,
        "msg": "success",
        "data": {"id": user.id, "nickname": user.nickname, "avatar_url": user.avatar_url},
    }


@router.get("/stats")
async def get_stats(db: DbSession, user_id: RequiredUserId):
    """用户本周阅读统计"""
    now = datetime.now(timezone.utc)
    week_start = now - timedelta(days=now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

    # 本周收藏数
    week_bookmarked = await db.scalar(
        select(func.count()).select_from(Bookmark).where(
            Bookmark.user_id == user_id,
            Bookmark.created_at >= week_start,
        )
    )

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "weekRead": 0,
            "weekBookmarked": week_bookmarked or 0,
            "weekSkipped": 0,
        },
    }
