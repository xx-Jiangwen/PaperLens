import httpx
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException
from jose import jwt
from sqlalchemy import select
from app.config import settings
from app.dependencies import DbSession
from app.models.user import User

router = APIRouter()


@router.post("/wx-login")
async def wx_login(body: dict, db: DbSession):
    """微信小程序登录。
    前端传入 wx.login() 获取的临时 code，
    后端换取 openid，生成 JWT Token 返回。
    """
    code = body.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="缺少 code 参数")

    # 调用微信 API 换取 openid
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.weixin.qq.com/sns/jscode2session",
            params={
                "appid": settings.WX_APP_ID,
                "secret": settings.WX_APP_SECRET,
                "js_code": code,
                "grant_type": "authorization_code",
            },
        )
    wx_data = resp.json()

    if "errcode" in wx_data and wx_data["errcode"] != 0:
        raise HTTPException(status_code=401, detail=f"微信登录失败: {wx_data.get('errmsg')}")

    openid = wx_data["openid"]
    union_id = wx_data.get("unionid")

    # 查找或创建用户
    result = await db.execute(select(User).where(User.openid == openid))
    user = result.scalar_one_or_none()

    if not user:
        user = User(openid=openid, union_id=union_id, source="miniprogram")
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        user.last_seen_at = datetime.now(timezone.utc)
        await db.commit()

    # 生成 JWT Token
    token = _create_token(user.id)
    return {"code": 200, "msg": "success", "data": {"token": token, "user_id": user.id}}


def _create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expire}, settings.SECRET_KEY, algorithm="HS256")
