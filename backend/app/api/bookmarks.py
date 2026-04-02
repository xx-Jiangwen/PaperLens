from fastapi import APIRouter, Query
from sqlalchemy import select, delete, func
from sqlalchemy.exc import IntegrityError
from app.dependencies import DbSession, RequiredUserId
from app.models.bookmark import Bookmark
from app.models.paper import Paper

router = APIRouter()


@router.get("")
async def list_bookmarks(
    db: DbSession,
    user_id: RequiredUserId,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    """获取收藏列表（含论文详情），支持分页"""
    # 计算总数
    count_stmt = select(func.count()).select_from(Bookmark).where(Bookmark.user_id == user_id)
    total = await db.scalar(count_stmt)

    # 分页查询
    offset = (page - 1) * size
    stmt = (
        select(Bookmark, Paper)
        .join(Paper, Bookmark.paper_id == Paper.id)
        .where(Bookmark.user_id == user_id)
        .order_by(Bookmark.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    result = await db.execute(stmt)
    rows = result.all()
    data = [
        {
            "bookmarked_at": bm.created_at.isoformat(),
            "note": bm.note,
            "paper": {
                "id": p.id,
                "title": p.title,
                "authors": p.authors,
                "categories": p.categories,
                "published_at": p.published_at.isoformat() if p.published_at else None,
                "summary_status": p.summary_status,
            },
        }
        for bm, p in rows
    ]
    return {"code": 200, "msg": "success", "data": data, "total": total}


@router.post("/{paper_id}")
async def add_bookmark(paper_id: str, db: DbSession, user_id: RequiredUserId):
    try:
        db.add(Bookmark(user_id=user_id, paper_id=paper_id))
        await db.commit()
        return {"code": 200, "msg": "收藏成功", "data": None}
    except IntegrityError:
        await db.rollback()
        return {"code": 200, "msg": "已收藏", "data": None}


@router.delete("/{paper_id}")
async def remove_bookmark(paper_id: str, db: DbSession, user_id: RequiredUserId):
    await db.execute(
        delete(Bookmark).where(Bookmark.user_id == user_id, Bookmark.paper_id == paper_id)
    )
    await db.commit()
    return {"code": 200, "msg": "已取消收藏", "data": None}
