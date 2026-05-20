"""
评论路由模块
处理评论列表、详情、统计、回复等接口
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.response import paginated, success
from app.models.user import User
from app.schemas.review import (
    BatchDeleteRequest,
    QuickReplyRequest,
    ReviewCreateRequest,
    ReviewFilterParams,
    ReviewResponse,
    ReviewStatsResponse,
    ReviewUpdateRequest,
    SimilarReviewResponse,
)
from app.services import review_service

router = APIRouter(prefix="/reviews", tags=["评价管理"])


@router.get("", summary="评价列表")
async def get_reviews(
    sentiment: str | None = Query(None, description="情感: positive/negative/neutral"),
    keyword: str | None = Query(None, description="关键词搜索"),
    store_id: UUID | None = Query(None, description="门店ID"),
    platform: str | None = Query(None, description="来源平台"),
    rating_min: int | None = Query(None, ge=1, le=5, description="最低评分"),
    rating_max: int | None = Query(None, ge=1, le=5, description="最高评分"),
    has_reply: bool | None = Query(None, description="是否有回复"),
    has_image: bool | None = Query(None, description="是否有图片"),
    start_date: str | None = Query(None, description="开始日期(YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="结束日期(YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取评价列表
    - 支持按情感、平台、评分、关键词等条件筛选
    - 根据用户角色过滤可见评论
    """
    filters = {
        "sentiment": sentiment,
        "keyword": keyword,
        "store_id": store_id,
        "platform": platform,
        "rating_min": rating_min,
        "rating_max": rating_max,
        "has_reply": has_reply,
        "has_image": has_image,
        "start_date": start_date,
        "end_date": end_date,
        "page": page,
        "page_size": page_size,
    }

    reviews, total = await review_service.get_reviews(db, current_user, filters)

    items = []
    for review in reviews:
        review_data = ReviewResponse.model_validate(review).model_dump(mode="json")
        # 填充门店名称
        if review.store:
            review_data["store_name"] = review.store.name
        items.append(review_data)

    return paginated(items=items, total=total, page=page, page_size=page_size)


@router.get("/stats", summary="评价统计")
async def get_review_stats(
    period: str = Query("30d", description="统计周期: 7d/30d/90d/all"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取评价统计数据
    - 包含总数、情感分布、平均评分、回复率等
    """
    stats = await review_service.get_review_stats(db, current_user, period)

    return success(
        data=ReviewStatsResponse(**stats).model_dump(mode="json"),
    )


@router.get("/{review_id}", summary="评价详情")
async def get_review_detail(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取评价详情
    """
    review = await review_service.get_review_by_id(db, review_id)

    review_data = ReviewResponse.model_validate(review).model_dump(mode="json")
    if review.store:
        review_data["store_name"] = review.store.name

    return success(data=review_data)


@router.get("/{review_id}/similar", summary="相似评论")
async def get_similar_reviews(
    review_id: UUID,
    limit: int = Query(5, ge=1, le=20, description="返回数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取相似评论列表
    - 基于相同门店和情感，按评分相近排序
    """
    reviews = await review_service.get_similar_reviews(db, review_id, limit)

    items = []
    for idx, review in enumerate(reviews):
        data = SimilarReviewResponse(
            id=review.id,
            user_name=review.user_name,
            content=review.content,
            rating=review.rating,
            sentiment=review.sentiment,
            similarity_score=round(1.0 - idx * 0.15, 2),  # 简化的相似度计算
        ).model_dump(mode="json")
        items.append(data)

    return success(data=items)


@router.post("", summary="新增评价")
async def create_review(
    request: ReviewCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    新增评价（爬虫入库用）
    """
    review = await review_service.create_review(db, request.model_dump())

    return success(
        data=ReviewResponse.model_validate(review).model_dump(mode="json"),
        message="评价创建成功",
    )


@router.put("/{review_id}", summary="更新评价")
async def update_review(
    review_id: UUID,
    request: ReviewUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    更新评价信息
    - 可更新回复内容和状态
    """
    review = await review_service.update_review(
        db, review_id, request.model_dump(exclude_none=True)
    )

    return success(
        data=ReviewResponse.model_validate(review).model_dump(mode="json"),
        message="评价更新成功",
    )


@router.delete("/{review_id}", summary="删除评价")
async def delete_review(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    删除评价（软删除）
    """
    await review_service.delete_review(db, review_id)

    return success(message="评价已删除")


@router.post("/batch-delete", summary="批量删除评价")
async def batch_delete_reviews(
    request: BatchDeleteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    批量删除评价（软删除）
    """
    count = await review_service.batch_delete_reviews(db, request.ids)

    return success(data={"deleted_count": count}, message=f"已删除 {count} 条评价")


@router.post("/{review_id}/like", summary="赞同评论")
async def like_review(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    赞同评论
    """
    review = await review_service.like_review(db, review_id)

    return success(message="操作成功")


@router.post("/{review_id}/reply", summary="快速回复")
async def quick_reply(
    review_id: UUID,
    request: QuickReplyRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    快速回复评论
    """
    review = await review_service.quick_reply(
        db, review_id, request.reply_content, current_user.id
    )

    return success(
        data=ReviewResponse.model_validate(review).model_dump(mode="json"),
        message="回复成功",
    )


@router.post("/{review_id}/approve-reply", summary="审核通过并发送回复")
async def approve_reply(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    审核通过 AI 回复并发送
    - 将 AI 回复草稿设为正式回复
    """
    audit = await review_service.approve_reply(db, review_id, current_user.id)

    return success(
        data={
            "id": str(audit.id),
            "status": audit.status,
            "reviewed_at": audit.reviewed_at.isoformat() if audit.reviewed_at else None,
        },
        message="回复已审核通过并发送",
    )
