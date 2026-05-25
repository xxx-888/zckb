"""
订阅相关 Schema
定义订阅计划、用户订阅等请求/响应数据结构
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SubscriptionPlanResponse(BaseModel):
    """订阅计划响应"""

    id: UUID
    name: str
    price_monthly: float
    price_yearly: float
    features: Optional[list[str]] = None
    max_stores: int
    max_reviews_per_month: Optional[int] = None
    is_active: bool

    model_config = {"from_attributes": True}


class UserSubscriptionResponse(BaseModel):
    """用户订阅响应"""

    id: UUID
    plan: SubscriptionPlanResponse
    status: str
    start_date: date
    end_date: Optional[date] = None
    auto_renew: bool

    model_config = {"from_attributes": True}


class UpgradeRequest(BaseModel):
    """升级订阅请求"""

    plan_id: UUID = Field(..., description="目标套餐ID")


class SubscriptionPlanCreateRequest(BaseModel):
    """创建订阅套餐请求"""

    name: str = Field(..., min_length=1, max_length=100, description="套餐名称")
    price_monthly: float = Field(0.0, ge=0, description="月价格")
    price_yearly: float = Field(0.0, ge=0, description="年价格")
    features: Optional[list[str]] = Field(None, description="功能特性列表")
    max_stores: int = Field(1, ge=1, description="最大门店数")
    max_reviews_per_month: Optional[int] = Field(None, ge=0, description="每月最大评论数")
    is_active: bool = Field(True, description="是否启用")


class SubscriptionPlanUpdateRequest(BaseModel):
    """更新订阅套餐请求"""

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="套餐名称")
    price_monthly: Optional[float] = Field(None, ge=0, description="月价格")
    price_yearly: Optional[float] = Field(None, ge=0, description="年价格")
    features: Optional[list[str]] = Field(None, description="功能特性列表")
    max_stores: Optional[int] = Field(None, ge=1, description="最大门店数")
    max_reviews_per_month: Optional[int] = Field(None, ge=0, description="每月最大评论数")
    is_active: Optional[bool] = Field(None, description="是否启用")


class PaymentRecordResponse(BaseModel):
    """支付记录响应"""

    id: UUID
    user_id: UUID
    subscription_id: Optional[UUID] = None
    amount: float
    payment_method: str
    status: str
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CreatePaymentRequest(BaseModel):
    """创建支付请求"""

    plan_id: UUID = Field(..., description="套餐ID")
    payment_method: str = Field(..., description="支付方式: wechat/alipay")
    billing_cycle: str = Field("yearly", description="计费周期: monthly/yearly")
