"""通知相关模型：NotificationChannel、NotificationRule、NotificationHistory、NotificationTemplate。"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, GUID


class NotificationChannel(BaseModel):
    """通知渠道表。"""

    __tablename__ = "notification_channels"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="渠道名称"
    )
    type: Mapped[str] = mapped_column(
        Enum(
            "wechat", "dingtalk", "feishu", "email", "sms", "push",
            name="notification_channel_type",
        ),
        nullable=False,
        comment="渠道类型: wechat/dingtalk/feishu/email/sms/push",
    )
    webhook_url: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="Webhook URL"
    )
    config: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="渠道配置(JSON)"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否启用"
    )

    # -- 关系 --
    rules: Mapped[list[NotificationRule]] = relationship(
        "NotificationRule", back_populates="channel", lazy="selectin"
    )
    histories: Mapped[list[NotificationHistory]] = relationship(
        "NotificationHistory", back_populates="channel", lazy="selectin"
    )


class NotificationRule(BaseModel):
    """通知规则表。"""

    __tablename__ = "notification_rules"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="规则名称"
    )
    channel_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("notification_channels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="渠道ID",
    )
    event_type: Mapped[str] = mapped_column(
        Enum(
            "new_review", "negative_alert", "weekly_report", "spider_status",
            name="notification_event_type",
        ),
        nullable=False,
        comment="事件类型: new_review/negative_alert/weekly_report/spider_status",
    )
    condition: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="触发条件(JSON)"
    )
    frequency: Mapped[str] = mapped_column(
        Enum("realtime", "daily", "weekly", name="notification_frequency"),
        nullable=False,
        default="realtime",
        comment="频率: realtime-实时, daily-每日, weekly-每周",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否启用"
    )

    # -- 关系 --
    channel: Mapped[NotificationChannel] = relationship(
        "NotificationChannel", back_populates="rules"
    )
    histories: Mapped[list[NotificationHistory]] = relationship(
        "NotificationHistory", back_populates="rule", lazy="selectin"
    )


class NotificationHistory(BaseModel):
    """通知历史记录表。"""

    __tablename__ = "notification_histories"

    rule_id: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("notification_rules.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="规则ID",
    )
    channel_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("notification_channels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="渠道ID",
    )
    title: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="通知标题"
    )
    content: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="通知内容"
    )
    recipient: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="接收者"
    )
    status: Mapped[str] = mapped_column(
        Enum("pending", "sent", "failed", name="notification_history_status"),
        nullable=False,
        default="pending",
        comment="状态: pending-待发送, sent-已发送, failed-发送失败",
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="错误信息"
    )
    latency_ms: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="发送延迟(毫秒)"
    )

    # -- 关系 --
    rule: Mapped[Optional[NotificationRule]] = relationship(
        "NotificationRule", back_populates="histories"
    )
    channel: Mapped[NotificationChannel] = relationship(
        "NotificationChannel", back_populates="histories"
    )


class NotificationTemplate(BaseModel):
    """通知模板表。"""

    __tablename__ = "notification_templates"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="模板名称"
    )
    event_type: Mapped[str] = mapped_column(
        Enum(
            "new_review", "negative_alert", "weekly_report", "spider_status",
            name="notification_template_event_type",
        ),
        nullable=False,
        comment="事件类型",
    )
    template_text: Mapped[str] = mapped_column(
        Text, nullable=False, comment="模板文本"
    )
    variables: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, comment="变量列表"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否启用"
    )
