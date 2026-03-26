from sqlalchemy import Column, Integer, String, Boolean, Text, JSON, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.models.base import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id                = Column(Integer,      primary_key=True, autoincrement=True)
    user_id           = Column(Integer,      ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # BYOK LLM 配置（api_key 加密存储）
    llm_base_url      = Column(String(512),  nullable=True)
    llm_api_key_enc   = Column(Text,         nullable=True)   # AES-256-GCM 密文
    llm_model_name    = Column(String(128),  nullable=True)

    # 阅读偏好
    preferred_categories = Column(JSON,       nullable=True, default=list)
    language          = Column(String(8),    nullable=False, default="zh")
    daily_digest      = Column(Boolean,      nullable=False, default=True)

    created_at        = Column(DateTime,     nullable=False, server_default=func.now())
    updated_at        = Column(DateTime,     nullable=False, server_default=func.now(),
                               onupdate=func.now())

    __table_args__ = (UniqueConstraint("user_id"),)
