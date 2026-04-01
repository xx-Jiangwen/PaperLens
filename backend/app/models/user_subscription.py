from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from app.models.base import Base


class UserSubscription(Base):
    """用户订阅状态，用于每日论文推送"""
    __tablename__ = "user_subscriptions"

    id              = Column(Integer,    primary_key=True, autoincrement=True)
    user_id         = Column(Integer,    ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    # 订阅类型：daily_papers / bookmark_reminder / summary_ready
    subscribe_type  = Column(String(32), nullable=False, default="daily_papers")
    # 是否启用推送
    enabled         = Column(Boolean,     nullable=False, default=False)
    # 可用推送次数（微信订阅消息是一次性的，用户每次订阅增加次数）
    push_quota      = Column(Integer,     nullable=False, default=0)
    # 用户在小程序端订阅时选择的模板ID
    template_id     = Column(String(64),  nullable=True)
    # 最后一次推送时间
    last_pushed_at  = Column(DateTime,    nullable=True)
    created_at      = Column(DateTime,    nullable=False, server_default=func.now())
    updated_at      = Column(DateTime,    nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_user_subscriptions_user", "user_id"),
    )