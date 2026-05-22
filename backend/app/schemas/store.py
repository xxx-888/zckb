"""
门店相关 Schema
定义门店、门店平台、门店统计等请求/响应数据结构
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class StorePlatformResponse(BaseModel):
    """门店平台关联响应"""

    id: UUID
    platform: str
    platform_store_id: Optional[str] = None
    platform_store_name: Optional[str] = None
    connected: bool
    last_sync_at: Optional[datetime] = None
    sync_status: Optional[str] = None

    model_config = {"from_attributes": True}


class StoreResponse(BaseModel):
    """门店响应"""

    id: UUID
    name: str
    type: str
    address: Optional[str] = None
    owner_name: Optional[str] = None
    owner_id: Optional[UUID] = None
    phone: Optional[str] = None
    status: str
    health_score: Optional[float] = None
    platform_count: int
    review_count: int
    region_id: Optional[UUID] = None
    platforms: list[StorePlatformResponse] = []
    created_at: datetime

    model_config = {"from_attributes": True}


class StoreCreateRequest(BaseModel):
    """新增门店请求"""

    name: str = Field(..., description="门店名称", min_length=1, max_length=255)
    type: str = Field(..., description="门店类型: restaurant/hotel/beverage")
    address: Optional[str] = Field(None, description="门店地址", max_length=500)
    owner_name: Optional[str] = Field(None, description="店主姓名", max_length=100)
    owner_id: Optional[UUID] = Field(None, description="负责人ID（关联用户表）")
    phone: Optional[str] = Field(None, description="联系电话", max_length=20)


class StoreUpdateRequest(BaseModel):
    """更新门店请求"""

    name: Optional[str] = Field(None, description="门店名称", min_length=1, max_length=255)
    type: Optional[str] = Field(None, description="门店类型: restaurant/hotel/beverage")
    address: Optional[str] = Field(None, description="门店地址", max_length=500)
    owner_name: Optional[str] = Field(None, description="店主姓名", max_length=100)
    owner_id: Optional[UUID] = Field(None, description="负责人ID（关联用户表）")
    phone: Optional[str] = Field(None, description="联系电话", max_length=20)
    status: Optional[str] = Field(None, description="门店状态: active/pending/inactive")


class StoreListResponse(BaseModel):
    """门店列表响应"""

    items: list[StoreResponse]
    total: int
    page: int
    pageSize: int


class StoreReviewStats(BaseModel):
    """门店评价统计"""

    total_reviews: int = 0
    avg_rating: float = 0.0
    positive_rate: float = 0.0
    negative_rate: float = 0.0
    reply_rate: float = 0.0
    sentiment_distribution: dict = {}


class StoreMonthlyStats(BaseModel):
    """门店月度统计"""

    month: str
    total_reviews: int = 0
    avg_rating: float = 0.0
    positive_count: int = 0
    negative_count: int = 0
    reply_count: int = 0
