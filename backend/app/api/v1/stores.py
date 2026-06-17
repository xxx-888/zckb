"""
门店路由模块
处理门店的增删改查、统计、激活等接口
"""

import logging
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

logger = logging.getLogger(__name__)

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


@router.post("/{store_id}/sync-reviews", summary="同步门店评论数据")
async def sync_store_reviews(
    store_id: UUID,
    current_user: User = Depends(require_valid_subscription),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    智能增量同步指定门店的平台评论数据。

    自动检测用户关联的平台账号：
    - 只关联了抖音来客 → 只同步抖音评论
    - 关联了美团开店宝 → 同步美团+点评评论
    - 都关联了 → 同步全平台评论

    采用增量同步（近30天），自动去重。
    """
    from sqlalchemy import select
    from app.models.store import StorePlatform, PlatformAccount
    from app.services.review_sync_service import ReviewSyncService
    from app.services.platform_service import PlatformService
    from app.core.exceptions import NotFoundException

    # 验证店铺归属
    store = await store_service.get_store_by_id(db, store_id)

    # 获取该店铺绑定的所有平台账号
    stmt = select(StorePlatform).where(
        StorePlatform.store_id == store_id,
        StorePlatform.account_id.isnot(None),
    )
    result = await db.execute(stmt)
    store_platforms = result.scalars().all()

    if not store_platforms:
        return success(data={"created": 0, "skipped": 0, "total": 0}, message="该店铺暂未绑定平台账号")

    # 按 account_id 分组，去重
    account_ids = list({str(sp.account_id) for sp in store_platforms if sp.account_id})

    # 为每个账号触发增量同步
    total_created = 0
    total_skipped = 0
    synced_platforms = set()

    review_service = ReviewSyncService.get_instance()
    platform_service = PlatformService(db)

    for account_id_str in account_ids:
        from uuid import UUID as UUIDType
        account_id_uuid = UUIDType(account_id_str)

        # 获取平台账号
        account = await platform_service.get_account_by_id(account_id_uuid)
        if not account or not account.cookies_encrypted:
            logger.warning(f"[sync_store_reviews] Account {account_id_str}: no cookies, skipping")
            continue

        # 解密 cookies
        storage_state = await platform_service._decrypt_credentials(account.cookies_encrypted)
        if not storage_state or not isinstance(storage_state, dict) or not storage_state.get("cookies"):
            logger.warning(f"[sync_store_reviews] Account {account_id_str}: invalid storage_state, skipping")
            continue

        # 获取该账号下所有绑定店铺
        all_sp_stmt = select(StorePlatform).where(
            StorePlatform.account_id == account.id,
            StorePlatform.store_id.isnot(None),
        )
        all_sp_result = await db.execute(all_sp_stmt)
        all_store_platforms = all_sp_result.scalars().all()

        # 按 platform 分组店铺
        stores_by_platform: dict[str, list] = {}
        for sp in all_store_platforms:
            if not sp.platform_store_id:
                continue
            store_info = {
                "platform_store_id": sp.platform_store_id,
                "platform_store_name": sp.platform_store_name,
                "store_id": str(sp.store_id) if sp.store_id else "",
            }
            # 抖音需要 life_account_id
            if sp.platform == "douyin" and account.platform_account_id:
                store_info["account_id"] = account.platform_account_id
            stores_by_platform.setdefault(sp.platform, []).append(store_info)

        if not stores_by_platform:
            continue

        # 增量同步（近30天）
        time_type = "近30天"

        for platform, stores in stores_by_platform.items():
            if platform in synced_platforms:
                continue

            logger.info(f"[sync_store_reviews] 开始同步: account={account_id_str}, platform={platform}, stores={len(stores)}")

            try:
                sync_result = await review_service.sync_reviews(
                    platform=platform,
                    storage_state=storage_state,
                    stores=stores,
                    time_type=time_type,
                )

                if sync_result.get("status") == "success":
                    platform_reviews = sync_result.get("reviews", [])
                    logger.info(f"[sync_store_reviews] {platform} 返回 {len(platform_reviews)} 条评论")

                    # 去重入库
                    from app.models.review import Review
                    platform_review_ids = [r.get("platform_review_id") for r in platform_reviews if r.get("platform_review_id")]
                    existing_ids = set()
                    if platform_review_ids:
                        exist_stmt = select(Review.platform_review_id).where(
                            Review.platform_review_id.in_(platform_review_ids),
                        )
                        exist_result = await db.execute(exist_stmt)
                        existing_ids = set(exist_result.scalars().all())

                    created_count = 0
                    for raw in platform_reviews:
                        feedback_id = raw.get("platform_review_id")
                        if not feedback_id or feedback_id in existing_ids:
                            total_skipped += 1
                            continue

                        # 匹配门店
                        poi_id = raw.get("platform_store_id")
                        store_id_for_review = None
                        for p in all_store_platforms:
                            if p.platform_store_id == poi_id:
                                store_id_for_review = p.store_id
                                break

                        if not store_id_for_review:
                            total_skipped += 1
                            continue

                        review = Review(
                            store_id=store_id_for_review,
                            platform=raw.get("platform", "unknown"),
                            platform_review_id=feedback_id,
                            user_name=raw.get("user_name", "匿名用户"),
                            user_avatar=raw.get("user_avatar"),
                            rating=raw.get("rating", 3),
                            content=raw.get("content", ""),
                            images=raw.get("images", []),
                            sentiment=raw.get("sentiment", "neutral"),
                            platform_created_at=raw.get("platform_created_at"),
                        )
                        db.add(review)
                        created_count += 1

                    await db.commit()
                    total_created += created_count
                else:
                    logger.warning(f"[sync_store_reviews] {platform} 同步失败: {sync_result.get('error', 'unknown')}")
            except Exception as e:
                logger.error(f"[sync_store_reviews] {platform} 同步异常: {e}", exc_info=True)
                continue

            synced_platforms.add(platform)

    platform_names = {
        "meituan": "美团",
        "dianping": "大众点评",
        "douyin": "抖音",
    }
    synced_names = [platform_names.get(p, p) for p in synced_platforms]

    return success(
        data={
            "created": total_created,
            "skipped": total_skipped,
            "total": total_created + total_skipped,
            "platforms": list(synced_platforms),
        },
        message=f"评论增量同步完成（{'+'.join(synced_names)}），新增 {total_created} 条",
    )
