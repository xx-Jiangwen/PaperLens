from fastapi import APIRouter
from app.api import papers, ai, auth, users, settings, bookmarks

api_router = APIRouter()

api_router.include_router(papers.router,    prefix="/papers",    tags=["论文"])
api_router.include_router(ai.router,        prefix="/ai",        tags=["AI 摘要"])
api_router.include_router(auth.router,      prefix="/auth",      tags=["认证"])
api_router.include_router(users.router,     prefix="/users",     tags=["用户"])
api_router.include_router(settings.router,  prefix="/settings",  tags=["用户设置"])
api_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["收藏"])
