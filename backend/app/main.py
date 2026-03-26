from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.models.base import Base
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：初始化数据库表、启动定时任务
    from app.db import engine
    from app.scheduler.setup import start_scheduler

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    scheduler = start_scheduler()

    yield

    # 关闭时：停止定时任务
    scheduler.shutdown()


app = FastAPI(
    title="PaperPulse API",
    description="每日脉动，掌握前沿 — arXiv 论文聚合 + AI 结构化摘要",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境替换为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
