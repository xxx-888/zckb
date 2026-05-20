"""
AI分析路由模块
处理移动端AI分析相关接口
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.response import paginated, success
from app.models.user import User
from app.schemas.ai_analysis import (
    AppealSuggestionResponse,
    ReplyHistoryResponse,
    ReplyStatsResponse,
    RiskLevelsResponse,
    SentimentSummaryResponse,
    TagClusterResponse,
    TopicResponse,
)
from app.services import ai_analysis_service

router = APIRouter(prefix="/ai-analysis", tags=["AI分析"])


@router.get("/topics", summary="语义分析主题")
async def get_topics(
    period: str = Query("30d", description="时间周期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取语义分析主题
    - 分析评论中的热点话题
    - 返回主题标签、情感倾向、提及次数等
    """
    topics = await ai_analysis_service.get_topics(db, current_user, period)
    return success(
        data=[TopicResponse(**topic).model_dump(mode="json") for topic in topics]
    )


@router.get("/tag-clustering", summary="差评标签聚类")
async def get_tag_clustering(
    period: str = Query("30d", description="时间周期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取差评标签聚类分析
    - 对差评内容进行标签分类
    - 返回各类别占比和趋势
    """
    clusters = await ai_analysis_service.get_tag_clustering(db, current_user, period)
    return success(
        data=[TagClusterResponse(**cluster).model_dump(mode="json") for cluster in clusters]
    )


@router.get("/sentiment-summary", summary="情感指数")
async def get_sentiment_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取情感指数汇总
    - 正面/负面评价统计
    - AI识别准确率
    """
    summary = await ai_analysis_service.get_sentiment_summary(db, current_user)
    return success(data=SentimentSummaryResponse(**summary).model_dump(mode="json"))


@router.get("/risk-levels", summary="风险分级")
async def get_risk_levels(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取风险分级统计
    - 高/中/低风险评论数量
    - 各级别处理建议
    """
    levels = await ai_analysis_service.get_risk_levels(db, current_user)
    return success(data=RiskLevelsResponse(**levels).model_dump(mode="json"))


@router.get("/reply-history", summary="自动回复历史")
async def get_reply_history(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取自动回复历史记录
    - 包含AI生成和人工回复
    - 支持分页查询
    """
    history, total = await ai_analysis_service.get_reply_history(
        db, current_user, page, page_size
    )
    return paginated(
        items=[ReplyHistoryResponse(**item).model_dump(mode="json") for item in history],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/reply-stats", summary="回复统计")
async def get_reply_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取回复统计数据
    - 总回复数
    - AI生成vs人工回复比例
    - 成功率统计
    """
    stats = await ai_analysis_service.get_reply_stats(db, current_user)
    return success(data=ReplyStatsResponse(**stats).model_dump(mode="json"))


@router.get("/appeal-suggestions/{review_id}", summary="申诉建议")
async def get_appeal_suggestion(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取申诉建议
    - AI分析评论是否为恶意差评
    - 提供申诉文案建议
    """
    suggestion = await ai_analysis_service.get_appeal_suggestion(db, review_id)
    return success(data=AppealSuggestionResponse(**suggestion).model_dump(mode="json"))
