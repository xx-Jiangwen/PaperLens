from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id           = Column(Integer,      primary_key=True, autoincrement=True)
    openid       = Column(String(128),  unique=True, nullable=True)   # 微信 openid
    union_id     = Column(String(128),  nullable=True)
    nickname     = Column(String(64),   nullable=True)
    avatar_url   = Column(String(512),  nullable=True)
    source       = Column(String(16),   nullable=False, default="miniprogram")  # miniprogram | web
    is_active    = Column(Boolean,      nullable=False, default=True)
    created_at   = Column(DateTime,     nullable=False, server_default=func.now())
    last_seen_at = Column(DateTime,     nullable=False, server_default=func.now(),
                          onupdate=func.now())
