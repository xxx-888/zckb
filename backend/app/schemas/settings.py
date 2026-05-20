"""
设置相关 Schema
定义回复模板、自动回复配置、通知设置、用户信息等请求/响应数据结构
"""

from datetime import datetime, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ==================== 回复模板 ====================


class ReplyTemplateResponse(BaseModel):
    """回复模板响应"""

    id: UUID
    name: str
    type: str
    content: str
    variables: Optional[list[str]] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ReplyTemplateCreateRequest(BaseModel):
    """创建回复模板请求"""

    name: str = Field(..., description="模板名称", min_length=1, max_length=100)
    type: str = Field(..., description="模板类型: good/bad/neutral")
    content: str = Field(..., description="模板内容", min_length=1, max_length=2000)


class ReplyTemplateUpdateRequest(BaseModel):
    """更新回复模板请求"""

    name: Optional[str] = Field(None, description="模板名称", min_length=1, max_length=100)
    type: Optional[str] = Field(None, description="模板类型: good/bad/neutral")
    content: Optional[str] = Field(None, description="模板内容", min_length=1, max_length=2000)
    is_active: Optional[bool] = Field(None, description="是否启用")


# ==================== 自动回复配置 ====================


class AutoReplyConfigResponse(BaseModel):
    """自动回复配置响应"""

    id: UUID
    mode: str
    auto_reply_enabled: bool
    work_hours_only: bool
    work_start_time: Optional[time] = None
    work_end_time: Optional[time] = None
    keyword_reply_enabled: bool
    keywords: Optional[dict] = None
    ai_suggest_enabled: bool

    model_config = {"from_attributes": True}


class AutoReplyConfigUpdateRequest(BaseModel):
    """更新自动回复配置请求"""

    mode: Optional[str] = Field(None, description="模式: smart/semi_auto/manual")
    auto_reply_enabled: Optional[bool] = Field(None, description="是否启用自动回复")
    work_hours_only: Optional[bool] = Field(None, description="仅工作时间回复")
    work_start_time: Optional[time] = Field(None, description="工作开始时间")
    work_end_time: Optional[time] = Field(None, description="工作结束时间")
    keyword_reply_enabled: Optional[bool] = Field(None, description="是否启用关键词回复")
    keywords: Optional[dict] = Field(None, description="关键词配置")
    ai_suggest_enabled: Optional[bool] = Field(None, description="是否启用AI建议")


# ==================== 用户通知设置 ====================


class UserNotificationSettingResponse(BaseModel):
    """用户通知设置响应"""

    id: UUID
    new_review_enabled: bool
    negative_alert_enabled: bool
    weekly_report_enabled: bool
    email_enabled: bool
    sms_enabled: bool
    push_enabled: bool
    quiet_hours_start: Optional[time] = None
    quiet_hours_end: Optional[time] = None

    model_config = {"from_attributes": True}


class UserNotificationSettingUpdateRequest(BaseModel):
    """更新用户通知设置请求"""

    new_review_enabled: Optional[bool] = Field(None, description="新评论通知")
    negative_alert_enabled: Optional[bool] = Field(None, description="差评预警通知")
    weekly_report_enabled: Optional[bool] = Field(None, description="周报通知")
    email_enabled: Optional[bool] = Field(None, description="邮件通知")
    sms_enabled: Optional[bool] = Field(None, description="短信通知")
    push_enabled: Optional[bool] = Field(None, description="推送通知")
    quiet_hours_start: Optional[time] = Field(None, description="免打扰开始时间")
    quiet_hours_end: Optional[time] = Field(None, description="免打扰结束时间")


# ==================== 用户信息 ====================


class UserInfoResponse(BaseModel):
    """用户信息响应"""

    id: UUID
    phone: Optional[str] = None
    email: Optional[str] = None
    username: str
    role: str
    avatar: Optional[str] = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserInfoUpdateRequest(BaseModel):
    """更新用户信息请求"""

    username: Optional[str] = Field(None, description="用户名", min_length=2, max_length=100)
    email: Optional[str] = Field(None, description="邮箱")
    avatar: Optional[str] = Field(None, description="头像URL")
