from fastapi import APIRouter
from sqlalchemy import select
from app.dependencies import DbSession, RequiredUserId
from app.models.user_subscription import UserSubscription

router = APIRouter()


@router.get("/status")
async def get_subscription_status(db: DbSession, user_id: RequiredUserId):
    """获取用户订阅状态"""
    result = await db.execute(
        select(UserSubscription).where(UserSubscription.user_id == user_id)
    )
    sub = result.scalar_one_or_none()

    if not sub:
        return {
            "code": 200,
            "msg": "success",
            "data": {
                "enabled": False,
                "push_quota": 0,
                "subscribe_type": "daily_papers",
            },
        }

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "enabled": sub.enabled,
            "push_quota": sub.push_quota,
            "subscribe_type": sub.subscribe_type,
            "last_pushed_at": sub.last_pushed_at.isoformat() if sub.last_pushed_at else None,
        },
    }


@router.post("/enable")
async def enable_subscription(body: dict, db: DbSession, user_id: RequiredUserId):
    """启用订阅推送"""
    template_id = body.get("template_id")

    result = await db.execute(
        select(UserSubscription).where(UserSubscription.user_id == user_id)
    )
    sub = result.scalar_one_or_none()

    if not sub:
        sub = UserSubscription(
            user_id=user_id,
            enabled=True,
            push_quota=1,
            template_id=template_id,
            subscribe_type="daily_papers",
        )
        db.add(sub)
    else:
        sub.enabled = True
        if template_id:
            sub.template_id = template_id
        # 用户重新订阅，增加推送配额
        sub.push_quota += 1

    await db.commit()
    return {"code": 200, "msg": "订阅成功", "data": {"push_quota": sub.push_quota}}


@router.post("/disable")
async def disable_subscription(db: DbSession, user_id: RequiredUserId):
    """禁用订阅推送"""
    result = await db.execute(
        select(UserSubscription).where(UserSubscription.user_id == user_id)
    )
    sub = result.scalar_one_or_none()

    if sub:
        sub.enabled = False
        await db.commit()

    return {"code": 200, "msg": "已取消订阅", "data": None}


@router.post("/add-quota")
async def add_push_quota(body: dict, db: DbSession, user_id: RequiredUserId):
    """用户在小程序端订阅消息后调用，增加推送配额"""
    template_id = body.get("template_id")
    count = body.get("count", 1)  # 用户可能同时订阅多个模板

    result = await db.execute(
        select(UserSubscription).where(UserSubscription.user_id == user_id)
    )
    sub = result.scalar_one_or_none()

    if not sub:
        sub = UserSubscription(
            user_id=user_id,
            enabled=True,
            push_quota=count,
            template_id=template_id,
            subscribe_type="daily_papers",
        )
        db.add(sub)
    else:
        sub.push_quota += count
        sub.enabled = True
        if template_id:
            sub.template_id = template_id

    await db.commit()
    return {"code": 200, "msg": "配额已更新", "data": {"push_quota": sub.push_quota}}