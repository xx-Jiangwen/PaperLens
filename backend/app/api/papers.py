from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy import select, desc, or_
from app.dependencies import DbSession
from app.models.paper import Paper
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
        stmt = stmt.where(
            or_(Paper.title.ilike(f"%{q}%"), Paper.abstract.ilike(f"%{q}%"))
        )

    offset = (page - 1) * size
    stmt = stmt.offset(offset).limit(size)
    result = await db.execute(stmt)
    papers = result.scalars().all()

    return {"code": 200, "msg": "success", "data": [_paper_out(p) for p in papers]}


@router.get("/today")
async def today_papers(db: DbSession):
    """今日新抓取论文"""
    from datetime import date, datetime, timezone
    today_start = datetime.combine(date.today(), datetime.min.time()).replace(tzinfo=timezone.utc)

    stmt = (
        select(Paper)
        .where(Paper.fetched_at >= today_start)
        .order_by(desc(Paper.published_at))
        .limit(50)
    )
    result = await db.execute(stmt)
    papers = result.scalars().all()
    return {"code": 200, "msg": "success", "data": [_paper_out(p) for p in papers]}


@router.get("/{paper_id}")
async def get_paper(paper_id: str, db: DbSession):
    """单篇论文详情"""
    result = await db.execute(select(Paper).where(Paper.id == paper_id))
    paper = result.scalar_one_or_none()
    if not paper:
        return {"code": 404, "msg": "论文不存在", "data": None}
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
