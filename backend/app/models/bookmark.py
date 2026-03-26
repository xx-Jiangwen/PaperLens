from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.sql import func
from app.models.base import Base


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id         = Column(Integer,     primary_key=True, autoincrement=True)
    user_id    = Column(Integer,     ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    paper_id   = Column(String(64),  ForeignKey("papers.id", ondelete="CASCADE"), nullable=False)
    note       = Column(Text,        nullable=True)   # 用户笔记（V2.0 预留）
    created_at = Column(DateTime,    nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "paper_id"),
        Index("idx_bookmarks_user_id", "user_id", "created_at"),
    )
