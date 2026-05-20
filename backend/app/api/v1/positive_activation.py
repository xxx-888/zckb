"""
好评激活路由模块
处理优质好评内容生成和授权相关接口
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.response import paginated, success
from app.models.user import User
from app.schemas.positive_activation import (
    BrandScriptResponse,
    GenerateContentRequest,
    GeneratedContentResponse,
    HighQualityReviewResponse,
)
from app.services import positive_activation_service

router = APIRouter(prefix="/positive-activation", tags=["好评激活"])


@router.get("/high-quality-reviews", summary="优质好评列表")
async def get_high_quality_reviews(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取优质好评列表
    - 筛选高评分、正面情感的评论
    - 可用于二次营销和内容生成
    """
    reviews, total = await positive_activation_service.get_high_quality_reviews(
        db, current_user, page, page_size
    )
    return paginated(
        items=[HighQualityReviewResponse(**review).model_dump(mode="json") for review in reviews],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/brand-scripts", summary="品牌话术库")
async def get_brand_scripts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取品牌话术库
    - 常用好评回复模板
    - 种草文案模板
    """
    scripts = await positive_activation_service.get_brand_scripts(db)
    return success(
        data=[BrandScriptResponse(**script).model_dump(mode="json") for script in scripts]
    )


@router.post("/copy-script/{script_id}", summary="记录话术复制")
async def copy_script(
    script_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    记录话术复制行为
    - 统计话术使用频率
    """
    await positive_activation_service.copy_script(db, script_id)
    return success(message="已记录")


@router.post("/send-authorization/{review_id}", summary="发送授权请求")
async def send_authorization(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    发送授权请求
    - 请求用户授权使用其评价内容
    - 用于二次营销
    """
    await positive_activation_service.send_authorization(db, review_id)
    return success(message="授权请求已发送")


@router.post("/generate-content", summary="生成种草内容")
async def generate_content(
    request: GenerateContentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    生成种草内容
    - 基于好评生成社交媒体内容
    - 支持小红书、抖音、微博等平台
    """
    content = await positive_activation_service.generate_content(
        db, request.review_id, request.platform
    )
    return success(data=GeneratedContentResponse(**content).model_dump(mode="json"))
