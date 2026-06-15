"""评论相关模型：Review、ReplyAudit。"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, GUID

if TYPE_CHECKING:
    from .ai_config import AIProcessingLog


class Review(BaseModel):
    """评论表。"""

    __tablename__ = "reviews"

    store_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="门店ID",
    )
    platform: Mapped[str] = mapped_column(
        Enum(
            "meituan", "dianping", "douyin", "taobao", "jd",
            name="review_platform",
        ),
        nullable=False,
        comment="来源平台",
    )
    platform_review_id: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="平台侧评论ID"
    )
    user_name: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="评论者昵称"
    )
    user_avatar: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="评论者头像URL"
    )
    rating: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="评分(1-5)"
    )
    content: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="评论内容"
    )
    images: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, comment="评论图片URL列表"
    )
    sentiment: Mapped[Optional[str]] = mapped_column(
        Enum("positive", "negative", "neutral", name="review_sentiment"),
        nullable=True,
        comment="情感分析: positive-正面, negative-负面, neutral-中性",
    )
    tags: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, comment="标签列表"
    )
    raw_json: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="原始爬虫数据"
    )
    reply: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="商家回复内容"
    )
    reply_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="回复时间"
    )
    ai_generated: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, comment="是否AI生成回复"
    )
    ai_reply_draft: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="AI回复草稿"
    )
    risk_level: Mapped[Optional[str]] = mapped_column(
        Enum("high", "medium", "low", name="review_risk_level"),
        nullable=True,
        comment="风险等级: high-高, medium-中, low-低",
    )
    status: Mapped[str] = mapped_column(
        Enum("normal", "appealed", "deleted", name="review_status"),
        nullable=False,
        default="normal",
        comment="状态: normal-正常, appealed-申诉中, deleted-已删除",
    )
    platform_created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="平台侧评论时间"
    )

    # -- 关系 --
    store: Mapped[Store] = relationship("Store", back_populates="reviews")
    reply_audits: Mapped[list[ReplyAudit]] = relationship(
        "ReplyAudit", back_populates="review", lazy="selectin"
    )
    processing_logs: Mapped[list[AIProcessingLog]] = relationship(
        "AIProcessingLog", back_populates="review", lazy="selectin"
    )


class ReplyAudit(BaseModel):
    """回复审核表。"""

    __tablename__ = "reply_audits"

    review_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("reviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="评论ID",
    )
    store_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="门店ID",
    )
    ai_reply_content: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="AI回复内容"
    )
    status: Mapped[str] = mapped_column(
        Enum("pending", "approved", "rejected", "sent", name="reply_audit_status"),
        nullable=False,
        default="pending",
        comment="审核状态: pending-待审核, approved-已通过, rejected-已拒绝, sent-已发送",
    )
    risk_level: Mapped[Optional[str]] = mapped_column(
        Enum("high", "medium", "low", name="audit_risk_level"),
        nullable=True,
        comment="风险等级",
    )
    scores: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        comment="评分: realism/empathy/concreteness/consistency",
    )
    reject_reason: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="拒绝原因"
    )
    auditor_id: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="审核人ID",
    )
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="审核时间"
    )

    # -- 关系 --
    review: Mapped[Review] = relationship("Review", back_populates="reply_audits")
    store: Mapped[Store] = relationship("Store")
