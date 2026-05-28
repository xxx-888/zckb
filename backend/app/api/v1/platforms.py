"""
平台关联路由模块
处理平台账号连接、店铺绑定、数据同步等平台关联相关接口
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_valid_subscription, get_db
from app.core.response import success, error, paginated
from app.models.user import User
from app.schemas.platform import (
    PlatformConnectRequest,
    PlatformConnectResponse,
    PlatformStoreInfo,
    PlatformBindRequest,
    PlatformSyncRequest,
    PlatformSyncResponse,
    PlatformAccountResponse,
    PlatformStoreResponse,
    SyncStatusResponse,
    PlatformReplyRequest,
    PlatformReplyResponse,
    PlatformDisconnectRequest,
)
from app.services.platform_service import PlatformService

router = APIRouter(prefix="/platforms", tags=["平台关联"])


@router.post("/connect", summary="连接平台账号")
async def connect_platform(
    request: PlatformConnectRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    连接平台账号
    - 验证平台账号凭证
    - 返回平台店铺列表
    """
    platform_service = PlatformService(db)

    credentials = {
        "username": request.username,
        "password": request.password,
        "verify_code": request.verify_code,
    }

    result = await platform_service.connect_platform(
        user_id=current_user.id,
        platform=request.platform,
        credentials=credentials,
    )

    return success(
        data=PlatformConnectResponse(
            success=result["success"],
            message=result["message"],
            stores=[
                PlatformStoreInfo(
                    platform_store_id=s["platform_store_id"],
                    platform_store_name=s["platform_store_name"],
                    platform=s["platform"],
                    rating=s["rating"],
                    review_count=s["review_count"],
                )
                for s in result["stores"]
            ],
        ).model_dump(mode="json"),
        message="平台账号连接成功",
    )


@router.get("/{platform}/stores", summary="获取平台店铺列表")
async def get_platform_stores(
    platform: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取平台店铺列表
    - 返回指定平台下的所有店铺
    """
    platform_service = PlatformService(db)

    # 使用模拟凭证获取店铺列表
    stores = await platform_service.get_platform_stores(platform, {})

    return success(
        data=[
            PlatformStoreInfo(
                platform_store_id=s["platform_store_id"],
                platform_store_name=s["platform_store_name"],
                platform=s["platform"],
                rating=s["rating"],
                review_count=s["review_count"],
            ).model_dump(mode="json")
            for s in stores
        ],
        message="获取成功",
    )


@router.post("/bind", summary="绑定平台店铺")
async def bind_platform_store(
    request: PlatformBindRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    绑定平台店铺
    - 将平台店铺与系统门店关联
    """
    platform_service = PlatformService(db)

    # 获取平台店铺信息
    stores = await platform_service.get_platform_stores("", {})
    platform_store = None
    for s in stores:
        if s["platform_store_id"] == request.platform_store_id:
            platform_store = s
            break

    if not platform_store:
        # 使用默认名称
        platform_store_name = f"平台店铺-{request.platform_store_id}"
    else:
        platform_store_name = platform_store["platform_store_name"]

    result = await platform_service.bind_platform_store(
        store_id=request.store_id,
        platform=platform_store["platform"] if platform_store else "meituan",
        platform_store_id=request.platform_store_id,
        platform_store_name=platform_store_name,
    )

    return success(
        data={
            "id": result.id,
            "store_id": result.store_id,
            "platform": result.platform,
            "platform_store_id": result.platform_store_id,
            "platform_store_name": result.platform_store_name,
            "connected": result.connected,
        },
        message="平台店铺绑定成功",
    )


@router.delete("/{store_platform_id}", summary="解绑平台店铺")
async def unbind_platform_store(
    store_platform_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    解绑平台店铺
    - 解除平台店铺与系统门店的关联
    """
    platform_service = PlatformService(db)
    await platform_service.unbind_platform_store(store_platform_id)

    return success(message="平台店铺解绑成功")


@router.post("/sync", summary="同步平台数据")
async def sync_platform_data(
    request: PlatformSyncRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    同步平台数据
    - 触发平台数据同步任务
    """
    platform_service = PlatformService(db)

    result = await platform_service.sync_platform_data(
        store_id=request.store_id,
        platform=request.platform,
        full_sync=request.full_sync,
    )

    return success(
        data=PlatformSyncResponse(
            task_id=result["task_id"],
            status=result["status"],
            message=result["message"],
        ).model_dump(mode="json"),
        message="同步任务已创建",
    )


@router.get("/sync-status/{store_platform_id}", summary="获取同步状态")
async def get_sync_status(
    store_platform_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取同步状态
    - 返回指定平台店铺的同步状态
    """
    platform_service = PlatformService(db)
    result = await platform_service.get_sync_status(store_platform_id)

    return success(
        data=SyncStatusResponse(
            store_platform_id=result["store_platform_id"],
            status=result["status"],
            progress=0,  # 可从任务中计算
            message=result["status"],
            last_sync_at=result["last_sync_at"],
            next_sync_at=result["next_sync_at"],
        ).model_dump(mode="json"),
        message="获取成功",
    )


@router.post("/{store_platform_id}/reply", summary="在平台上回复评论")
async def reply_on_platform(
    store_platform_id: UUID,
    request: PlatformReplyRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    在平台上回复评论
    - 将回复内容发送到对应平台
    """
    platform_service = PlatformService(db)

    sent = await platform_service.reply_on_platform(
        store_platform_id=store_platform_id,
        review_id=request.review_id,
        content=request.content,
    )

    return success(
        data=PlatformReplyResponse(
            success=sent,
            message="回复发送成功" if sent else "回复发送失败",
        ).model_dump(mode="json"),
        message="回复发送成功" if sent else "回复发送失败",
    )


@router.get("/accounts", summary="获取已连接的平台账号列表")
async def get_connected_accounts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取已连接的平台账号列表
    - 返回当前用户所有门店关联的平台账号
    """
    platform_service = PlatformService(db)
    platforms = await platform_service.get_connected_platforms(current_user)

    return success(
        data=[
            {
                "id": str(p["id"]),
                "platform": p["platform"],
                "platform_account": p["platform_store_name"],
                "connected": p["connected"],
                "last_sync_at": p["last_sync_at"],
            }
            for p in platforms
        ],
        message="获取成功",
    )


@router.get("/store/{store_platform_id}", summary="获取平台店铺详情")
async def get_platform_store_details(
    store_platform_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取平台店铺详情
    - 返回指定平台店铺的详细信息
    """
    platform_service = PlatformService(db)
    result = await platform_service.get_platform_store_details(store_platform_id)

    return success(
        data=PlatformStoreResponse(
            id=result["id"],
            store_id=result["store_id"],
            store_name=result["store_name"],
            platform=result["platform"],
            platform_store_id=result["platform_store_id"],
            platform_store_name=result["platform_store_name"],
            connected=result["connected"],
            last_sync_at=result["last_sync_at"],
            sync_status=result["sync_status"],
            review_count=result["review_count"],
        ).model_dump(mode="json"),
        message="获取成功",
    )


@router.post("/{store_platform_id}/refresh", summary="刷新平台Token")
async def refresh_platform_token(
    store_platform_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    刷新平台Token
    - 刷新指定平台店铺的访问令牌
    """
    platform_service = PlatformService(db)
    result = await platform_service.refresh_platform_token(store_platform_id)

    return success(
        data=result,
        message="Token刷新成功",
    )


@router.get("/statistics/overview", summary="获取平台统计概览")
async def get_platform_statistics(
    store_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取平台统计概览
    - 返回平台连接统计信息
    """
    platform_service = PlatformService(db)
    result = await platform_service.get_platform_statistics(store_id)

    return success(
        data=result,
        message="获取成功",
    )
