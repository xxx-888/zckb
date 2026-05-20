"""
平台关联相关 Schema
定义平台连接、店铺绑定、数据同步等请求/响应数据结构
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PlatformConnectRequest(BaseModel):
    """平台连接请求"""

    platform: str = Field(..., description="平台名称: meituan/dianping/douyin/taobao/jd")
    username: str = Field(..., description="平台账号用户名")
    password: str = Field(..., description="平台账号密码")
    verify_code: Optional[str] = Field(None, description="验证码（如需）")


class PlatformStoreInfo(BaseModel):
    """平台店铺信息"""

    platform_store_id: str = Field(..., description="平台侧门店ID")
    platform_store_name: str = Field(..., description="平台侧门店名称")
    platform: str = Field(..., description="平台名称")
    rating: float = Field(0.0, description="店铺评分")
    review_count: int = Field(0, description="评论数量")


class PlatformConnectResponse(BaseModel):
    """平台连接响应"""

    success: bool = Field(..., description="是否连接成功")
    message: str = Field(..., description="响应消息")
    stores: list[PlatformStoreInfo] = Field(default=[], description="平台店铺列表")


class PlatformBindRequest(BaseModel):
    """平台店铺绑定请求"""

    platform_store_id: str = Field(..., description="平台侧门店ID")
    store_id: UUID = Field(..., description="系统门店ID")


class PlatformSyncRequest(BaseModel):
    """平台数据同步请求"""

    store_id: UUID = Field(..., description="门店ID")
    platform: str = Field(..., description="平台名称")
    full_sync: bool = Field(False, description="是否全量同步")


class PlatformSyncResponse(BaseModel):
    """平台同步响应"""

    task_id: UUID = Field(..., description="同步任务ID")
    status: str = Field(..., description="任务状态: pending/processing/completed/failed")
    message: str = Field(..., description="状态消息")


class PlatformAccountResponse(BaseModel):
    """平台账号响应"""

    id: UUID = Field(..., description="账号ID")
    platform: str = Field(..., description="平台名称")
    platform_account: str = Field(..., description="平台账号")
    connected: bool = Field(..., description="是否已连接")
    last_sync_at: Optional[datetime] = Field(None, description="最后同步时间")


class PlatformStoreResponse(BaseModel):
    """平台店铺详情响应"""

    id: UUID = Field(..., description="关联记录ID")
    store_id: UUID = Field(..., description="系统门店ID")
    store_name: str = Field(..., description="门店名称")
    platform: str = Field(..., description="平台名称")
    platform_store_id: str = Field(..., description="平台侧门店ID")
    platform_store_name: str = Field(..., description="平台侧门店名称")
    connected: bool = Field(..., description="是否已连接")
    last_sync_at: Optional[datetime] = Field(None, description="最后同步时间")
    sync_status: Optional[str] = Field(None, description="同步状态")
    rating: Optional[float] = Field(None, description="平台评分")
    review_count: int = Field(0, description="平台评论数")

    model_config = {"from_attributes": True}


class SyncStatusResponse(BaseModel):
    """同步状态响应"""

    store_platform_id: UUID = Field(..., description="平台店铺关联ID")
    status: str = Field(..., description="同步状态: idle/syncing/error")
    progress: int = Field(0, description="同步进度(0-100)")
    message: str = Field("", description="状态消息")
    last_sync_at: Optional[datetime] = Field(None, description="最后同步时间")
    next_sync_at: Optional[datetime] = Field(None, description="下次同步时间")


class PlatformReplyRequest(BaseModel):
    """平台回复请求"""

    review_id: UUID = Field(..., description="评论ID")
    content: str = Field(..., description="回复内容", min_length=1, max_length=1000)


class PlatformReplyResponse(BaseModel):
    """平台回复响应"""

    success: bool = Field(..., description="是否发送成功")
    message: str = Field(..., description="响应消息")
    platform_message_id: Optional[str] = Field(None, description="平台消息ID")


class PlatformDisconnectRequest(BaseModel):
    """平台断开连接请求"""

    platform: str = Field(..., description="平台名称")
    confirm: bool = Field(..., description="确认断开")
