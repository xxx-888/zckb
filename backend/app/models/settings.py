"""设置相关模型：ReplyTemplate、AutoReplyConfig、UserNotificationSetting。"""

from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean, Enum, ForeignKey, JSON, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, GUID

if TYPE_CHECKING:
    from .user import User
    from .store import Store


class ReplyTemplate(BaseModel):
    """回复模板表。"""

    __tablename__ = "reply_templates"

    user_id: Mapped[Optional[str]] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="创建用户ID",
    )
    store_id: Mapped[Optional[str]] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="门店ID",
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="模板名称"
    )
    type: Mapped[str] = mapped_column(
        Enum("good", "bad", "neutral", name="reply_template_type"),
        nullable=False,
        comment="模板类型: good-好评, bad-差评, neutral-中性",
    )
    content: Mapped[str] = mapped_column(
        String(2000), nullable=False, comment="模板内容"
    )
    variables: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, comment="变量列表"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否启用"
    )

    # -- 关系 --
    user: Mapped[Optional[User]] = relationship("User", back_populates="reply_templates")


class AutoReplyConfig(BaseModel):
    """自动回复配置表。"""

    __tablename__ = "auto_reply_configs"

    store_id: Mapped[str] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
        comment="门店ID",
    )
    mode: Mapped[str] = mapped_column(
        Enum("smart", "semi_auto", "manual", name="auto_reply_mode"),
        nullable=False,
        default="semi_auto",
        comment="模式: smart-智能, semi_auto-半自动, manual-手动",
    )
    auto_reply_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, comment="是否启用自动回复"
    )
    work_hours_only: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="仅工作时间回复"
    )
    work_start_time: Mapped[Optional[time]] = mapped_column(
        Time, nullable=True, comment="工作开始时间"
    )
    work_end_time: Mapped[Optional[time]] = mapped_column(
        Time, nullable=True, comment="工作结束时间"
    )
    keyword_reply_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, comment="是否启用关键词回复"
    )
    keywords: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="关键词配置(JSON)"
    )
    ai_suggest_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否启用AI建议"
    )

    # -- 关系 --
    store: Mapped[Store] = relationship("Store", back_populates="auto_reply_config")


class UserNotificationSetting(BaseModel):
    """用户通知设置表。"""

    __tablename__ = "user_notification_settings"

    user_id: Mapped[str] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
        comment="用户ID",
    )
    new_review_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="新评论通知"
    )
    negative_alert_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="差评预警通知"
    )
    weekly_report_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="周报通知"
    )
    email_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, comment="邮件通知"
    )
    sms_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, comment="短信通知"
    )
    push_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="推送通知"
    )
    quiet_hours_start: Mapped[Optional[time]] = mapped_column(
        Time, nullable=True, comment="免打扰开始时间"
    )
    quiet_hours_end: Mapped[Optional[time]] = mapped_column(
        Time, nullable=True, comment="免打扰结束时间"
    )

    # -- 关系 --
    user: Mapped[User] = relationship(
        "User", back_populates="notification_setting"
    )
