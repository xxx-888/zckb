"""
Dashboard 路由模块
处理仪表盘核心统计、平台分布、门店排行等接口
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_valid_subscription
from app.core.response import success
from app.models.user import User
from app.schemas.dashboard import (
    CoreStatsResponse,
    HealthStatusResponse,
    PlatformDistributionResponse,
    RecentReviewResponse,
    StoreHealthResponse,
    StoreRankingResponse,
)
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["仪表盘"])


@router.get("/core-stats", summary="核心统计")
async def get_core_stats(
    period: str = Query("30d", description="统计周期: 7d/30d/90d"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取核心统计数据
    - 评论总数及趋势
    - 平均评分及趋势
    - 正面率及趋势
    - AI 回复率及趋势
    """
    stats = await dashboard_service.get_core_stats(db, current_user, period)

    return success(
        data=CoreStatsResponse(**stats).model_dump(mode="json"),
    )


@router.get("/platform-distribution", summary="平台分布")
async def get_platform_distribution(
    period: str = Query("30d", description="统计周期: 1d/7d/30d/90d"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取各平台评论分布数据
    - 包含各平台评论数量和占比
    """
    distribution = await dashboard_service.get_platform_distribution(db, current_user, period)

    items = [
        PlatformDistributionResponse(**item).model_dump(mode="json")
        for item in distribution
    ]

    return success(data=items)


@router.get("/recent-reviews", summary="最新评论")
async def get_recent_reviews(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取最新评论列表
    """
    reviews = await dashboard_service.get_recent_reviews(db, current_user, limit)

    items = []
    for review in reviews:
        data = RecentReviewResponse(
            id=review.id,
            store_name=review.store.name if review.store else None,
            user_name=review.user_name,
            content=review.content,
            rating=review.rating,
            sentiment=review.sentiment,
            platform=review.platform,
            time=review.created_at,
        ).model_dump(mode="json")
        items.append(data)

    return success(data=items)


@router.get("/store-rankings", summary="门店排行")
async def get_store_rankings(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取门店排行榜
    - 按平均评分降序排列
    """
    rankings = await dashboard_service.get_store_rankings(db, current_user, limit)

    items = [
        StoreRankingResponse(**item).model_dump(mode="json") for item in rankings
    ]

    return success(data=items)


@router.get("/health-status", summary="数据源健康")
async def get_health_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取各平台数据源健康状态
    - 根据最后同步时间判断状态
    """
    health_list = await dashboard_service.get_health_status(db, current_user)

    items = [
        HealthStatusResponse(**item).model_dump(mode="json") for item in health_list
    ]

    return success(data=items)


@router.get("/alert", summary="异常警告")
async def get_alerts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取异常警告列表
    - 高风险评论预警
    - 差评未回复提醒
    - AI 回复待审核
    - 评分下降预警
    """
    alerts = await dashboard_service.get_alerts(db, current_user)

    return success(data=alerts)


@router.get("/store-health", summary="门店健康值")
async def get_store_health(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取门店健康值列表
    - 包含健康评分、评论数、平均评分、回复率等
    """
    health_list = await dashboard_service.get_store_health(db, current_user)

    items = [
        StoreHealthResponse(**item).model_dump(mode="json") for item in health_list
    ]

    return success(data=items)
