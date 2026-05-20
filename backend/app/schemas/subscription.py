"""
订阅相关 Schema
定义订阅计划、用户订阅等请求/响应数据结构
"""

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SubscriptionPlanResponse(BaseModel):
    """订阅计划响应"""

    id: UUID
    name: str
    price_monthly: float
    price_yearly: float
    features: Optional[dict] = None
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
