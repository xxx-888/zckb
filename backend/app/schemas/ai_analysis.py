"""
AI分析模块Schema定义
用于移动端AI分析相关接口的请求和响应模型
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TopicResponse(BaseModel):
    """语义分析主题响应模型"""

    label: str = Field(..., description="主题标签")
    sentiment: str = Field(..., description="情感倾向: positive/negative/neutral")
    count: int = Field(..., description="提及次数")
    trend: str = Field(..., description="趋势: up/down/stable")


class TagClusterResponse(BaseModel):
    """差评标签聚类响应模型"""

    category: str = Field(..., description="标签分类")
    items: list[str] = Field(..., description="标签项列表")
    percentage: float = Field(..., description="占比百分比")
    color: str = Field(..., description="显示颜色")


class SentimentSummaryResponse(BaseModel):
    """情感指数响应模型"""

    score: float = Field(..., description="情感得分(0-100)")
    trend: str = Field(..., description="趋势: up/down/stable")
    positive: int = Field(..., description="正面评价数")
    negative: int = Field(..., description="负面评价数")
    ai_accuracy: float = Field(..., description="AI识别准确率")


class RiskLevelsResponse(BaseModel):
    """风险分级响应模型"""

    high_count: int = Field(..., description="高风险数量")
    high_desc: str = Field(..., description="高风险描述")
    medium_count: int = Field(..., description="中风险数量")
    medium_desc: str = Field(..., description="中风险描述")
    low_count: int = Field(..., description="低风险数量")
    low_desc: str = Field(..., description="低风险描述")


class ReplyHistoryResponse(BaseModel):
    """自动回复历史响应模型"""

    id: UUID = Field(..., description="记录ID")
    review_id: UUID = Field(..., description="评论ID")
    content: str = Field(..., description="回复内容")
    ai_generated: bool = Field(..., description="是否AI生成")
    status: str = Field(..., description="状态: pending/approved/rejected/sent")
    created_at: datetime = Field(..., description="创建时间")


class ReplyStatsResponse(BaseModel):
    """回复统计响应模型"""

    total: int = Field(..., description="总回复数")
    ai_generated: int = Field(..., description="AI生成数")
    manual: int = Field(..., description="手动回复数")
    success_rate: float = Field(..., description="成功率")


class AppealSuggestionResponse(BaseModel):
    """申诉建议响应模型"""

    review_id: UUID = Field(..., description="评论ID")
    is_malicious: bool = Field(..., description="是否为恶意差评")
    confidence: float = Field(..., description="置信度(0-1)")
    suggestion: str = Field(..., description="处理建议")
    appeal_content: str = Field(..., description="申诉文案")
