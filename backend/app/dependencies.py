from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from app.db import get_db
from app.config import settings

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)],
) -> Optional[int]:
    """从 JWT Token 解析用户 ID，未登录时返回 None（允许匿名访问）"""
    if credentials is None:
        return None
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        return int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        return None


async def require_user_id(
    user_id: Annotated[Optional[int], Depends(get_current_user_id)],
) -> int:
    """需要登录的接口使用此依赖，未登录抛 401"""
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录")
    return user_id


DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUserId = Annotated[Optional[int], Depends(get_current_user_id)]
RequiredUserId = Annotated[int, Depends(require_user_id)]
