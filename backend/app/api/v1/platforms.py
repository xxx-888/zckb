"""
平台关联路由模块
处理平台账号连接、店铺绑定、数据同步等平台关联相关接口
"""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.deps import require_valid_subscription, get_db, require_roles
from app.core.response import success, error, paginated
from app.core.exceptions import NotFoundException
from app.models.user import User
from app.models.store import PlatformAccount, StorePlatform
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
            account_id=result.get("account_id"),
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

    result = await platform_service.bind_platform_store(
        store_id=request.store_id,
        platform=request.platform,
        platform_store_id=request.platform_store_id,
        platform_store_name=request.platform_store_name,
        account_id=request.account_id,
    )

    return success(
        data={
            "id": str(result.id),
            "store_id": str(result.store_id),
            "platform": result.platform,
            "platform_store_id": result.platform_store_id,
            "platform_store_name": result.platform_store_name,
            "connected": result.connected,
        },
        message="平台店铺绑定成功",
    )


@router.delete("/store/{store_platform_id}", summary="解绑平台店铺")
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
            progress=0,
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
    - 返回当前用户的所有平台账号
    """
    platform_service = PlatformService(db)
    accounts = await platform_service.get_connected_platforms(current_user)

    return success(
        data=[
            {
                "id": str(a["id"]),
                "platform": a["platform"],
                "platform_username": a["platform_username"],
                "cookies_status": a.get("cookies_status", "unknown"),
                "last_sync_at": a.get("last_sync_at"),
            }
            for a in accounts
        ],
        message="获取成功",
    )


@router.post("/accounts/{account_id}/sync-status", summary="同步平台账号登录状态")
async def sync_account_status(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    同步平台账号登录状态
    - 将账号标记为 pending，等待爬虫服务更新状态
    - 普通用户只能同步自己的账号
    """
    platform_service = PlatformService(db)
    account = await platform_service.get_account_by_id(account_id)

    if not account or str(account.user_id) != str(current_user.id):
        raise NotFoundException("平台账号不存在")

    account.cookies_status = "pending"
    account.last_sync_at = datetime.utcnow()
    account.error_msg = None
    await db.commit()

    return success(message="已提交同步请求，请稍后刷新查看状态")


@router.put("/account/{account_id}", summary="更新平台账号")
async def update_platform_account(
    account_id: UUID,
    body: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    更新平台账号的用户名/密码
    - 普通用户只能修改自己的账号
    """
    platform_service = PlatformService(db)
    account = await platform_service.get_account_by_id(account_id)

    if not account or str(account.user_id) != str(current_user.id):
        raise NotFoundException("平台账号不存在")

    username = body.get("username")
    password = body.get("password")

    await platform_service.update_account(account_id, username=username, password=password)
    return success(message="修改成功")


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


# ============ 管理员接口 ============

@router.get("/admin/accounts", summary="管理员：获取所有用户的平台绑定账号")
async def admin_get_all_accounts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN")),
) -> dict:
    """
    管理员获取所有用户的平台绑定账号
    """
    from sqlalchemy.orm import selectinload

    stmt = (
        select(PlatformAccount)
        .options(selectinload(PlatformAccount.user))
        .order_by(PlatformAccount.created_at.desc())
    )
    result = await db.execute(stmt)
    accounts = result.scalars().all()

    data = []
    for acc in accounts:
        user_email = acc.user.email if acc.user else ""
        user_name = acc.user.username if acc.user else ""
        data.append({
            "id": str(acc.id),
            "user_id": str(acc.user_id) if acc.user_id else None,
            "user_email": user_email,
            "user_name": user_name,
            "platform": acc.platform,
            "platform_username": acc.platform_username or "",
            "cookies_status": acc.cookies_status or "unknown",
            "last_sync_at": acc.last_sync_at.isoformat() if acc.last_sync_at else None,
            "error_msg": acc.error_msg or "",
            "created_at": acc.created_at.isoformat() if acc.created_at else None,
        })

    return success(data=data, message="获取成功")


@router.delete("/account/{account_id}", summary="管理员：解绑平台账号")
async def admin_unbind_account(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN")),
) -> dict:
    """
    管理员解绑指定平台账号
    """
    stmt = select(PlatformAccount).where(PlatformAccount.id == account_id)
    result = await db.execute(stmt)
    account = result.scalar_one_or_none()

    if not account:
        raise NotFoundException("平台账号不存在")

    await db.delete(account)
    await db.commit()

    return success(message="解绑成功")


@router.post("/account/{account_id}/refresh", summary="管理员：刷新账号 Cookies")
async def admin_refresh_cookies(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN")),
) -> dict:
    """
    管理员刷新指定账号的 Cookies
    """
    stmt = select(PlatformAccount).where(PlatformAccount.id == account_id)
    result = await db.execute(stmt)
    account = result.scalar_one_or_none()

    if not account:
        raise NotFoundException("平台账号不存在")

    # 标记状态为 pending，等待爬虫服务处理
    account.cookies_status = "pending"
    account.last_sync_at = datetime.utcnow()
    account.error_msg = None
    await db.commit()

    return success(message="已标记为待刷新，等待爬虫服务处理")
