from sqlalchemy import Column, String, Text, JSON, DateTime, Index
from sqlalchemy.sql import func
from app.models.base import Base


class Paper(Base):
    __tablename__ = "papers"

    # 主键：含版本号，如 "arxiv:1706.03762v7"
    id               = Column(String(64),  primary_key=True)
    arxiv_id_base    = Column(String(32),  nullable=False)   # 去重键，如 "1706.03762"
    title            = Column(Text,        nullable=False)
    authors          = Column(JSON,        nullable=False, default=list)
    abstract         = Column(Text,        nullable=False)
    published_at     = Column(DateTime,    nullable=False)
    updated_at       = Column(DateTime,    nullable=True)
    url              = Column(String(256), nullable=True)
    pdf_url          = Column(String(256), nullable=True)
    categories       = Column(JSON,        nullable=True, default=list)
    primary_category = Column(String(32),  nullable=True)
    comment          = Column(Text,        nullable=True)
    journal_ref      = Column(String(256), nullable=True)
    doi              = Column(String(128), nullable=True)
    source_name      = Column(String(32),  nullable=False, default="arxiv")

    # AI 摘要（三段式）
    summary_what     = Column(Text,        nullable=True)
    summary_how      = Column(Text,        nullable=True)
    summary_why      = Column(Text,        nullable=True)
    # pending | processing | done | failed
    summary_status   = Column(String(16),  nullable=False, default="pending")
    summary_model    = Column(String(64),  nullable=True)

    fetched_at       = Column(DateTime,    nullable=False, server_default=func.now())
    created_at       = Column(DateTime,    nullable=False, server_default=func.now())
    updated_db_at    = Column(DateTime,    nullable=False, server_default=func.now(),
                              onupdate=func.now())

    __table_args__ = (
        Index("idx_papers_published_at", "published_at"),
        Index("idx_papers_primary_category", "primary_category"),
        Index("idx_papers_arxiv_id_base", "arxiv_id_base"),
        Index("idx_papers_summary_status", "summary_status"),
    )

    def has_summary(self) -> bool:
        return self.summary_status == "done"
