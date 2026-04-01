from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from app.models.base import Base


class ReadingLog(Base):
    """用户阅读记录，用于统计 weekRead"""
    __tablename__ = "reading_logs"

    id         = Column(Integer,    primary_key=True, autoincrement=True)
    user_id    = Column(Integer,    ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    paper_id   = Column(String(64), ForeignKey("papers.id", ondelete="CASCADE"), nullable=False)
    viewed_at  = Column(DateTime,   nullable=False, server_default=func.now())

    __table_args__ = (
        Index("idx_reading_logs_user_viewed", "user_id", "viewed_at"),
    )