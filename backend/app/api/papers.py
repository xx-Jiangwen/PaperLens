from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy import select, desc, or_, func
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
    # 构建基础查询
    stmt = select(Paper)
    count_stmt = select(func.count(Paper.id))

    if category:
        stmt = stmt.where(Paper.primary_category == category)
        count_stmt = count_stmt.where(Paper.primary_category == category)
    if q:
        escaped_q = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        pattern = f"%{escaped_q}%"
        stmt = stmt.where(
            or_(Paper.title.ilike(pattern), Paper.abstract.ilike(pattern))
        )
        count_stmt = count_stmt.where(
            or_(Paper.title.ilike(pattern), Paper.abstract.ilike(pattern))
        )

    # 获取总数
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # 分页查询
    stmt = stmt.order_by(desc(Paper.published_at))
    offset = (page - 1) * size
    stmt = stmt.offset(offset).limit(size)
    result = await db.execute(stmt)
    papers = result.scalars().all()

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "items": [_paper_out(p) for p in papers],
            "total": total,
            "page": page,
            "size": size,
            "hasMore": offset + len(papers) < total,
        },
    }


@router.get("/today")
async def today_papers(
    db: DbSession,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    """一周精选论文（最近 7 天发表的）"""
    from datetime import datetime, timedelta, timezone

    week_ago = datetime.now(timezone.utc) - timedelta(days=7)

    # 获取总数
    count_stmt = select(func.count(Paper.id)).where(Paper.published_at >= week_ago)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # 分页查询
    offset = (page - 1) * size
    stmt = (
        select(Paper)
        .where(Paper.published_at >= week_ago)
        .order_by(desc(Paper.published_at))
        .offset(offset)
        .limit(size)
    )
    result = await db.execute(stmt)
    papers = result.scalars().all()

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "items": [_paper_out(p) for p in papers],
            "total": total,
            "page": page,
            "size": size,
            "hasMore": offset + len(papers) < total,
        },
    }


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
