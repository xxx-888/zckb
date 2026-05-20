"""
经营洞察模块Schema定义
用于经营分析和洞察相关接口的请求和响应模型
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class DishResponse(BaseModel):
    """菜品口碑响应模型"""

    name: str = Field(..., description="菜品名称")
    score: float = Field(..., description="口碑得分")
    positive: int = Field(..., description="好评数")
    negative: int = Field(..., description="差评数")
    type: str = Field(..., description="类型: recommend/improve/eliminate")


class ThreeGoodThreeBadResponse(BaseModel):
    """三好三差报告响应模型"""

    goods: list[str] = Field(..., description="三项优点")
    bads: list[str] = Field(..., description="三项不足")


class DishEliminationResponse(BaseModel):
    """末位淘汰建议响应模型"""

    name: str = Field(..., description="菜品名称")
    score: float = Field(..., description="综合得分")
    reason: str = Field(..., description="淘汰原因")
    suggestion: str = Field(..., description="改进建议")


class ServiceCaseResponse(BaseModel):
    """服务案例响应模型"""

    id: UUID = Field(..., description="案例ID")
    type: str = Field(..., description="案例类型: complaint/praise/suggestion")
    content: str = Field(..., description="案例内容")
    store_name: Optional[str] = Field(None, description="门店名称")
    created_at: datetime = Field(..., description="创建时间")


class CompetitorOpportunityResponse(BaseModel):
    """同行机会洞察响应模型"""

    title: str = Field(..., description="机会标题")
    description: str = Field(..., description="机会描述")
    action_items: list[str] = Field(..., description="行动建议")
