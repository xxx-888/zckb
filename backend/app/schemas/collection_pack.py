"""
采集套餐相关 Schema
定义采集套餐、采集订单的请求/响应数据结构
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ==================== 采集套餐 Schema ====================

class CollectionPackResponse(BaseModel):
    """采集套餐响应"""

    id: UUID
    name: str
    credit_amount: int
    price: float
    description: Optional[str] = None
    is_active: bool

    model_config = {"from_attributes": True}


class CollectionPackCreateRequest(BaseModel):
    """创建采集套餐请求"""

    name: str = Field(..., min_length=1, max_length=100, description="套餐名称")
    credit_amount: int = Field(..., ge=1, description="积分数量（条）")
    price: float = Field(..., ge=0, description="价格（元）")
    description: Optional[str] = Field(None, max_length=255, description="套餐描述")
    is_active: bool = Field(True, description="是否启用")


class CollectionPackUpdateRequest(BaseModel):
    """更新采集套餐请求"""

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="套餐名称")
    credit_amount: Optional[int] = Field(None, ge=1, description="积分数量（条）")
    price: Optional[float] = Field(None, ge=0, description="价格（元）")
    description: Optional[str] = Field(None, max_length=255, description="套餐描述")
    is_active: Optional[bool] = Field(None, description="是否启用")


# ==================== 采集订单 Schema ====================

class CollectionOrderResponse(BaseModel):
    """采集订单响应"""

    id: UUID
    user_id: UUID
    user_name: str
    email: str
    pack_id: UUID
    pack_name: str
    credit_amount: int
    amount: float
    payment_method: str
    status: str
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class CreateCollectionOrderRequest(BaseModel):
    """创建采集订单请求"""

    pack_id: UUID = Field(..., description="套餐ID")
    payment_method: str = Field(..., description="支付方式: wechat/alipay")


# ==================== 用户积分余额 Schema ====================

class UserCollectionBalanceResponse(BaseModel):
    """用户积分余额响应"""

    user_id: UUID
    balance: int
    total_purchased: int

    model_config = {"from_attributes": True}
