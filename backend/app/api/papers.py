from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy import select, desc, or_
from app.dependencies import DbSession, CurrentUserId
from app.models.paper import Paper
from app.models.reading_log import ReadingLog
from app.sources.arxiv_source import ArxivSource

router = APIRouter()


@router.get("")
async def list_papers(
    db: DbSession,
    category: Optional[str] = None,
    q: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    """论文列表，支持分类筛选和关键词搜索"""
    stmt = select(Paper).order_by(desc(Paper.published_at))

    if category:
        stmt = stmt.where(Paper.primary_category == category)
    if q:
        # 转义 LIKE 特殊字符，防止用户输入 % 或 _ 影响匹配
        escaped_q = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        pattern = f"%{escaped_q}%"
        stmt = stmt.where(
            or_(Paper.title.ilike(pattern), Paper.abstract.ilike(pattern))
        )

    offset = (page - 1) * size
    stmt = stmt.offset(offset).limit(size)
    result = await db.execute(stmt)
    papers = result.scalars().all()

    return {"code": 200, "msg": "success", "data": [_paper_out(p) for p in papers]}


@router.get("/today")
async def today_papers(db: DbSession):
    """最新论文（最近 7 天发表的）"""
    from datetime import datetime, timedelta, timezone

    # 最近 7 天发表的论文，按发表时间倒序
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    stmt = (
        select(Paper)
        .where(Paper.published_at >= week_ago)
        .order_by(desc(Paper.published_at))
        .limit(50)
    )
    result = await db.execute(stmt)
    papers = result.scalars().all()
    return {"code": 200, "msg": "success", "data": [_paper_out(p) for p in papers]}


@router.get("/{paper_id}")
async def get_paper(paper_id: str, db: DbSession, user_id: CurrentUserId):
    """单篇论文详情"""
    result = await db.execute(select(Paper).where(Paper.id == paper_id))
    paper = result.scalar_one_or_none()
    if not paper:
        return {"code": 404, "msg": "论文不存在", "data": None}

    # 记录阅读行为（已登录用户）
    if user_id:
        db.add(ReadingLog(user_id=user_id, paper_id=paper_id))
        await db.commit()

    return {"code": 200, "msg": "success", "data": _paper_out(paper)}


@router.post("/search")
async def search_papers(body: dict):
    """透传 arXiv 实时搜索（不经过数据库）"""
    query = body.get("q", "")
    max_results = min(body.get("max", 10), 50)
    if not query:
        return {"code": 400, "msg": "请提供搜索关键词", "data": None}

    source = ArxivSource()
    papers = await source.search(query, max_results=max_results)
    return {"code": 200, "msg": "success", "data": [p.__dict__ for p in papers]}


def _paper_out(p: Paper) -> dict:
    return {
        "id": p.id,
        "title": p.title,
        "authors": p.authors,
        "abstract": p.abstract,
        "published_at": p.published_at.isoformat() if p.published_at else None,
        "categories": p.categories,
        "primary_category": p.primary_category,
        "url": p.url,
        "pdf_url": p.pdf_url,
        "comment": p.comment,
        "summary_status": p.summary_status,
        "summary_what": p.summary_what,
        "summary_how": p.summary_how,
        "summary_why": p.summary_why,
    }
