"""
爬虫相关 Schema
定义爬虫平台、同步日志、任务等请求/响应数据结构
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SpiderPlatformResponse(BaseModel):
    """爬虫平台响应"""

    id: UUID
    name: str
    display_name: str
    status: str
    reliability: float
    error_log: Optional[str] = None
    config: Optional[dict] = None
    last_sync_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class SpiderPlatformCreateRequest(BaseModel):
    """创建爬虫平台请求"""

    name: str = Field(..., description="平台名称: meituan/dianping/douyin/taobao/jd")
    display_name: str = Field(..., description="显示名称", min_length=1, max_length=100)
    config: Optional[dict] = Field(None, description="配置(JSONB，含cookies等)")


class SpiderPlatformUpdateRequest(BaseModel):
    """更新爬虫平台请求"""

    display_name: Optional[str] = Field(None, description="显示名称", max_length=100)
    status: Optional[str] = Field(None, description="状态: active/paused/error")
    config: Optional[dict] = Field(None, description="配置(JSONB，含cookies等)")


class SpiderSyncLogResponse(BaseModel):
    """爬虫同步日志响应"""

    id: UUID
    platform_id: UUID
    store_id: Optional[UUID] = None
    status: str
    records_synced: int
    error_message: Optional[str] = None
    duration_ms: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class SpiderTaskResponse(BaseModel):
    """爬虫任务响应"""

    id: int
    platform_id: UUID
    store_id: Optional[UUID] = None
    task_type: str
    status: str
    priority: int
    result: Optional[dict] = None
    error_message: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class SpiderTaskCreateRequest(BaseModel):
    """创建爬虫任务请求"""

    platform_id: UUID = Field(..., description="平台ID")
    store_id: Optional[UUID] = Field(None, description="门店ID")
    task_type: str = Field(..., description="任务类型: full_sync/incremental/reply")
    priority: int = Field(0, description="优先级", ge=0, le=100)
    scheduled_at: Optional[datetime] = Field(None, description="计划执行时间")


class SpiderPlatformListResponse(BaseModel):
    """爬虫平台列表响应"""

    items: list[SpiderPlatformResponse]
    total: int
    page: int
    pageSize: int


class SpiderSyncLogListResponse(BaseModel):
    """爬虫同步日志列表响应"""

    items: list[SpiderSyncLogResponse]
    total: int
    page: int
    pageSize: int


class SpiderTaskListResponse(BaseModel):
    """爬虫任务列表响应"""

    items: list[SpiderTaskResponse]
    total: int
    page: int
    pageSize: int


class SpiderTestConnectionResponse(BaseModel):
    """测试平台连接响应"""

    success: bool
    message: str
    response_time_ms: Optional[int] = None
