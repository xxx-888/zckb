"""
门店路由模块
处理门店的增删改查、统计、激活等接口
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_valid_subscription, get_db
from app.core.response import paginated, success
from app.models.user import User
from app.schemas.store import (
    StoreCreateRequest,
    StoreResponse,
    StoreUpdateRequest,
)
from app.services import store_service

router = APIRouter(prefix="/stores", tags=["门店管理"])


@router.get("", summary="门店列表")
async def get_stores(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(20, ge=1, le=100, description="每页数量"),
    type: Optional[str] = Query(None, description="门店类型: restaurant/hotel/beverage"),
    status: Optional[str] = Query(None, description="门店状态: active/pending/inactive"),
    keyword: Optional[str] = Query(None, description="搜索关键词（名称/地址）"),
    current_user: User = Depends(require_valid_subscription),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    获取门店列表
    - 支持按类型、状态筛选
    - 支持关键词搜索（名称/地址）
    - HQ 角色查看全部，OPERATOR/STORE 角色查看关联门店
    """
    stores, total = await store_service.get_stores(
        db,
        user=current_user,
        page=page,
        page_size=pageSize,
        type=type,
        status=status,
        keyword=keyword,
    )

    return paginated(
        items=[
            StoreResponse.model_validate(store).model_dump(mode="json")
            for store in stores
        ],
        total=total,
        page=page,
        page_size=pageSize,
    )


@router.get("/stats", summary="门店汇总统计")
async def get_stores_stats(
    current_user: User = Depends(require_valid_subscription),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    获取用户可访问门店的汇总统计
    - 包含门店总数、各状态数量、评论总数、类型分布等
    """
    stats = await store_service.get_stores_stats(db, current_user)
    return success(data=stats)


@router.get("/{store_id}", summary="门店详情")
async def get_store_detail(
    store_id: UUID,
    current_user: User = Depends(require_valid_subscription),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    获取门店详细信息
    - 包含门店基本信息和关联平台信息
    """
    store = await store_service.get_store_by_id(db, store_id)

    return success(
        data=StoreResponse.model_validate(store).model_dump(mode="json"),
    )


@router.post("", summary="新增门店")
async def create_store(
    request: StoreCreateRequest,
    current_user: User = Depends(require_valid_subscription),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    新增门店
    - 创建门店记录，默认状态为 pending
    """
    store = await store_service.create_store(db, request.model_dump())

    return success(
        data=StoreResponse.model_validate(store).model_dump(mode="json"),
        message="门店创建成功",
    )


@router.put("/{store_id}", summary="更新门店")
async def update_store(
    store_id: UUID,
    request: StoreUpdateRequest,
    current_user: User = Depends(require_valid_subscription),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    更新门店信息
    - 仅更新请求中提供的字段
    """
    store = await store_service.update_store(
        db, store_id, request.model_dump(exclude_unset=True)
    )

    return success(
        data=StoreResponse.model_validate(store).model_dump(mode="json"),
        message="门店更新成功",
    )


@router.delete("/{store_id}", summary="删除门店")
async def delete_store(
    store_id: UUID,
    current_user: User = Depends(require_valid_subscription),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    删除门店
    - 同时删除关联的平台配置和评论数据
    """
    await store_service.delete_store(db, store_id)

    return success(message="门店删除成功")


@router.post("/{store_id}/activate", summary="激活门店")
async def activate_store(
    store_id: UUID,
    current_user: User = Depends(require_valid_subscription),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    激活门店
    - 将门店状态从 pending 更新为 active
    """
    store = await store_service.activate_store(db, store_id)

    return success(
        data=StoreResponse.model_validate(store).model_dump(mode="json"),
        message="门店激活成功",
    )


@router.get("/{store_id}/review-stats", summary="门店评价统计")
async def get_store_review_stats(
    store_id: UUID,
    period: Optional[str] = Query("all", description="统计周期: 7d/30d/90d/all"),
    current_user: User = Depends(require_valid_subscription),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    获取门店评价统计数据
    - 包含评论总数、平均评分、情感分布、回复率等
    - 支持按周期筛选
    """
    stats = await store_service.get_store_review_stats(db, store_id, period)

    return success(data=stats)


@router.get("/{store_id}/monthly-stats", summary="门店月度统计")
async def get_store_monthly_stats(
    store_id: UUID,
    current_user: User = Depends(require_valid_subscription),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    获取门店月度统计数据
    - 返回最近12个月的评论统计
    - 包含每月评论数、平均评分、正负面数量、回复数
    """
    stats = await store_service.get_store_monthly_stats(db, store_id)

    return success(data=stats)


@router.get("/{store_id}/recent-reviews", summary="门店最近评论")
async def get_store_recent_reviews(
    store_id: UUID,
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    current_user: User = Depends(require_valid_subscription),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    获取门店最近评论
    - 按评论时间倒序排列
    - 默认返回最近10条
    """
    reviews = await store_service.get_store_recent_reviews(db, store_id, limit)

    review_list = []
    for review in reviews:
        review_list.append({
            "id": str(review.id),
            "platform": review.platform,
            "user_name": review.user_name,
            "rating": review.rating,
            "content": review.content,
            "sentiment": review.sentiment,
            "reply": review.reply,
            "ai_generated": review.ai_generated,
            "created_at": review.created_at.isoformat() if review.created_at else None,
        })

    return success(data=review_list)
