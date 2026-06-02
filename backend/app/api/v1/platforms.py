"""
平台关联路由模块
处理平台账号连接、店铺绑定、数据同步等平台关联相关接口
"""

from datetime import datetime
import json
import logging
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
from app.services.qr_login_service import QRLoginService
from app.services.sms_login_service import SMSLoginService
from app.services.store_sync_service import StoreSyncService

router = APIRouter(prefix="/platforms", tags=["平台关联"])
logger = logging.getLogger(__name__)

# 二维码登录服务实例
qr_login_service = QRLoginService.get_instance()
# 短信验证码登录服务实例
sms_login_service = SMSLoginService.get_instance()
# 店铺同步服务实例
store_sync_service = StoreSyncService.get_instance()


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


@router.get("/accounts/{account_id}/stores", summary="获取账号下已同步的店铺列表")
async def get_account_stores(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取指定平台账号下已同步的平台店铺列表（从 store_platforms 表查询）。
    """
    # 验证账号归属
    platform_service = PlatformService(db)
    account = await platform_service.get_account_by_id(account_id)
    if not account or str(account.user_id) != str(current_user.id):
        raise NotFoundException("平台账号不存在")

    stmt = select(StorePlatform).where(
        StorePlatform.account_id == account_id,
    ).order_by(StorePlatform.created_at.desc())
    result = await db.execute(stmt)
    store_platforms = result.scalars().all()

    data = []
    for sp in store_platforms:
        data.append({
            "id": str(sp.id),
            "store_id": str(sp.store_id) if sp.store_id else None,
            "platform": sp.platform,
            "platform_store_id": sp.platform_store_id or "",
            "platform_store_name": sp.platform_store_name or "",
            "connected": sp.connected,
            "sync_status": sp.sync_status,
            "last_sync_at": sp.last_sync_at.isoformat() if sp.last_sync_at else None,
            "binded": bool(sp.store_id),
        })

    return success(data=data, message="获取成功")


@router.post("/{platform}/stores", summary="获取平台店铺列表")
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


@router.post("/accounts/{account_id}/sync-status", summary="同步平台账号登录状态及店铺数据")
async def sync_account_status(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    同步平台账号：
    1. 验证登录态是否有效
    2. 如果有效，同步店铺列表（platform_store_id + platform_store_name）
    3. 更新 PlatformAccount 状态
    """
    platform_service = PlatformService(db)
    account = await platform_service.get_account_by_id(account_id)

    if not account or str(account.user_id) != str(current_user.id):
        raise NotFoundException("平台账号不存在")

    platform = account.platform

    # 解密获取 storage_state
    try:
        credentials = await platform_service._decrypt_credentials(account.cookies_encrypted)
    except Exception:
        account.cookies_status = "expired"
        account.error_msg = "凭证解密失败"
        await db.commit()
        return success(data={"status": "expired", "error": "凭证解密失败"}, message="同步完成")

    storage_state = credentials.get("cookies", {}).get("_storage_state")
    if not storage_state:
        account.cookies_status = "expired"
        account.error_msg = "无有效登录态，请重新扫码登录"
        await db.commit()
        return success(data={"status": "expired", "error": "无有效登录态"}, message="同步完成")

    # 1) 验证登录态
    from app.services.session_validation_service import SessionValidationService
    validate_svc = SessionValidationService.get_instance()
    validate_result = await validate_svc.validate(platform, storage_state)

    if not validate_result.get("valid"):
        account.cookies_status = "expired"
        account.error_msg = validate_result.get("error", "登录态已失效")
        await db.commit()
        return success(
            data={"status": "expired", "error": account.error_msg},
            message="登录态已失效，请重新扫码绑定",
        )

    # 登录态有效 - 更新状态和用户名
    account.cookies_status = "valid"
    account.error_msg = None
    if validate_result.get("platform_username"):
        account.platform_username = validate_result["platform_username"]

    # 2) 同步店铺数据
    sync_result = await store_sync_service.sync_stores(
        platform, storage_state, platform_account_id=account.platform_account_id
    )
    logger.info(f"[SyncAccount] sync_result raw: {json.dumps(sync_result, ensure_ascii=False, default=str)[:2000]}")
    synced_stores = 0

    if sync_result.get("status") == "success" and sync_result.get("stores"):
        stores = sync_result["stores"]
        from sqlalchemy import select
        from app.models.store import StorePlatform, Store as StoreModel
        from app.models.user import UserStore

        # 平台后缀映射
        platform_suffix_map = {
            "meituan": " - 美团",
            "dianping": " - 大众点评",
            "douyin": " - 抖音",
            "taobao": " - 淘宝",
            "jd": " - 京东",
        }
        store_suffix = platform_suffix_map.get(platform, f" - {platform}")

        for store_info in stores:
            ps_id = store_info["platform_store_id"]
            ps_name = store_info["platform_store_name"]

            # 查找是否已存在 store_platform 记录
            stmt = select(StorePlatform).where(
                StorePlatform.account_id == account.id,
                StorePlatform.platform_store_id == ps_id,
            )
            existing_result = await db.execute(stmt)
            existing_sp = existing_result.scalar_one_or_none()

            if existing_sp:
                # 更新已有记录
                existing_sp.platform_store_name = ps_name
                existing_sp.last_sync_at = datetime.utcnow()

                # 如果还没关联系统门店，自动创建并绑定
                if not existing_sp.store_id:
                    auto_store_name = ps_name + store_suffix
                    new_store = StoreModel(
                        name=auto_store_name,
                        type="restaurant",
                        status="active",
                        platform_count=1,
                        owner_id=current_user.id,
                    )
                    db.add(new_store)
                    await db.flush()  # 获取 new_store.id
                    existing_sp.store_id = new_store.id
                    existing_sp.connected = True

                    # 创建 UserStore 关联
                    user_store = UserStore(
                        user_id=str(current_user.id),
                        store_id=str(new_store.id),
                    )
                    db.add(user_store)
            else:
                # 自动创建系统门店并绑定
                auto_store_name = ps_name + store_suffix
                new_store = StoreModel(
                    name=auto_store_name,
                    type="restaurant",
                    status="active",
                    platform_count=1,
                    owner_id=current_user.id,
                )
                db.add(new_store)
                await db.flush()  # 获取 new_store.id

                # 创建 UserStore 关联
                user_store = UserStore(
                    user_id=str(current_user.id),
                    store_id=str(new_store.id),
                )
                db.add(user_store)

                # 创建 store_platform 记录并直接绑定
                new_sp = StorePlatform(
                    account_id=account.id,
                    platform=platform,
                    platform_store_id=ps_id,
                    platform_store_name=ps_name,
                    store_id=new_store.id,
                    connected=True,
                    last_sync_at=datetime.utcnow(),
                    sync_status="synced",
                )
                db.add(new_sp)
            synced_stores += 1

    # 更新同步时间
    account.last_sync_at = datetime.utcnow()
    await db.commit()

    return success(
        data={
            "status": "valid",
            "platform_username": account.platform_username,
            "store_count": synced_stores,
            "sync_detail": {
                "method": sync_result.get("method"),
                "raw_store_count": sync_result.get("store_count", 0),
                "sync_status": sync_result.get("status"),
                "sync_error": sync_result.get("error"),
            },
            "stores": sync_result.get("stores", []) if sync_result.get("status") == "success" else [],
        },
        message=f"同步完成，{synced_stores} 个店铺已更新",
    )


@router.post("/accounts/{account_id}/sync-reviews", summary="同步平台评论数据")
async def sync_account_reviews(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    同步指定平台账号下所有店铺的评论数据。
    1. 获取该账号下所有 store_platforms
    2. 通过 Playwright 调用平台评论 API
    3. 将评论数据导入 reviews 表（自动去重）
    """
    from app.models.store import Store as StoreModel
    from app.models.review import Review
    from app.services.review_sync_service import ReviewSyncService

    platform_service = PlatformService(db)
    account = await platform_service.get_account_by_id(account_id)
    if not account or str(account.user_id) != str(current_user.id):
        raise NotFoundException("平台账号不存在")

    if not account.storage_state:
        return error(message="账号无登录态，请先扫码登录")

    # 获取已绑定的店铺列表
    stmt = select(StorePlatform).where(
        StorePlatform.account_id == account.id,
        StorePlatform.store_id.isnot(None),
    )
    result = await db.execute(stmt)
    store_platforms = result.scalars().all()

    if not store_platforms:
        return error(message="暂无已绑定的店铺，请先同步店铺列表")

    # 构建店铺列表传给子进程
    stores = [
        {
            "platform_store_id": sp.platform_store_id,
            "platform_store_name": sp.platform_store_name,
            "store_id": str(sp.store_id) if sp.store_id else "",
        }
        for sp in store_platforms
        if sp.platform_store_id
    ]

    storage_state = account.storage_state if isinstance(account.storage_state, dict) else json.loads(account.storage_state)

    # 调用评论同步服务（子进程 Playwright 抓取）
    review_service = ReviewSyncService.get_instance()
    sync_result = await review_service.sync_reviews(
        platform=account.platform,
        storage_state=storage_state,
        stores=stores,
    )

    if sync_result.get("status") != "success":
        return error(message=f"评论同步失败: {sync_result.get('error', '未知错误')}")

    # 将评论数据导入 DB
    raw_reviews = sync_result.get("reviews", [])
    created_count = 0
    skipped_count = 0

    # 预查已存在的 review（去重）
    if raw_reviews:
        existing_keys = set()
        # 按 platform 分组批量查
        from itertools import groupby
        sorted_reviews = sorted(raw_reviews, key=lambda r: (r["platform"], r["platform_review_id"]))
        for plat, group in groupby(sorted_reviews, key=lambda r: r["platform"]):
            review_ids = [r["platform_review_id"] for r in list(group)]
            if review_ids:
                exist_stmt = select(Review.platform_review_id).where(
                    Review.platform == plat,
                    Review.platform_review_id.in_(review_ids),
                )
                exist_result = await db.execute(exist_stmt)
                existing_keys.update((plat, row[0]) for row in exist_result.all())

        # 逐条创建
        from datetime import datetime
        for item in raw_reviews:
            key = (item["platform"], item["platform_review_id"])
            if key in existing_keys or not item["platform_review_id"]:
                skipped_count += 1
                continue

            # 解析时间
            platform_time = None
            if item.get("platform_created_at"):
                try:
                    platform_time = datetime.fromisoformat(item["platform_created_at"].replace("Z", "+00:00"))
                    # 转为 naive datetime (与项目其他代码一致)
                    platform_time = platform_time.replace(tzinfo=None)
                except Exception:
                    pass

            review = Review(
                store_id=item["store_id"],
                platform=item["platform"],
                platform_review_id=item["platform_review_id"],
                user_name=item.get("user_name"),
                user_avatar=item.get("user_avatar"),
                rating=item.get("rating", 3),
                content=item.get("content"),
                images=item.get("images"),
                sentiment=item.get("sentiment"),
                raw_json=item.get("raw_json"),
                platform_created_at=platform_time,
                status="normal",
            )
            db.add(review)
            created_count += 1

        await db.commit()

    return success(
        data={
            "created": created_count,
            "skipped": skipped_count,
            "total": len(raw_reviews),
            "store_count": sync_result.get("store_count", 0),
        },
        message=f"评论同步完成，新增 {created_count} 条，跳过 {skipped_count} 条重复",
    )


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


# ============ 二维码扫码登录接口 ============

@router.post("/qr-login/start", summary="启动二维码扫码登录")
async def start_qr_login(
    body: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    启动二维码扫码登录
    - 后端打开平台登录页，截取二维码图片返回给前端
    - 用户用手机 App 扫码后，后端自动检测登录状态
    """
    platform = body.get("platform", "")
    result = await qr_login_service.start_login(
        user_id=str(current_user.id),
        platform=platform,
    )

    if not result.get("success"):
        return error(message=result.get("error", "启动登录失败"))

    return success(
        data={
            "task_id": result["task_id"],
            "qr_image": result["qr_image"],
            "status": result["status"],
            "expires_in": result["expires_in"],
        },
        message="二维码已生成，请使用手机App扫码",
    )


@router.get("/qr-login/status/{task_id}", summary="查询二维码登录状态")
async def get_qr_login_status(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    查询二维码登录状态（前端轮询）
    - waiting_scan: 等待扫码
    - success: 登录成功（返回 cookies）
    - expired: 二维码过期
    - failed: 登录失败
    """
    status_result = await qr_login_service.get_status(task_id)

    if status_result["status"] == "success":
        # 登录成功 → 自动创建/更新 PlatformAccount
        platform_service = PlatformService(db)
        cookies = status_result["cookies"]
        platform = status_result["platform"]
        platform_username = status_result.get("platform_username", "")
        platform_account_id = status_result.get("platform_account_id", "")

        encrypted = await platform_service._encrypt_credentials({
            "username": platform_username,
            "cookies": cookies,
        })

        # 查找已有账号或创建新账号
        from sqlalchemy import select
        stmt = select(PlatformAccount).where(
            PlatformAccount.user_id == current_user.id,
            PlatformAccount.platform == platform,
        )
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.cookies_encrypted = encrypted
            existing.cookies_status = "valid"
            existing.platform_username = platform_username
            existing.platform_account_id = platform_account_id
            existing.last_sync_at = datetime.utcnow()
            existing.error_msg = None
        else:
            new_account = PlatformAccount(
                user_id=current_user.id,
                platform=platform,
                platform_username=platform_username,
                platform_account_id=platform_account_id,
                cookies_encrypted=encrypted,
                cookies_status="valid",
                last_sync_at=datetime.utcnow(),
            )
            db.add(new_account)

        await db.commit()

        return success(
            data={
                "status": "success",
                "platform": platform,
                "platform_username": platform_username,
            },
            message="登录成功，账号已绑定",
        )

    return success(data=status_result)


@router.post("/qr-login/cancel/{task_id}", summary="取消二维码登录")
async def cancel_qr_login(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """取消二维码登录任务"""
    result = await qr_login_service.cancel_login(task_id)
    return success(message="已取消" if result.get("success") else result.get("error", "取消失败"))


# ============ 短信验证码登录（抖音来客） ============

from pydantic import BaseModel


class SmsStartRequest(BaseModel):
    platform: str
    phone: str


class SmsVerifyRequest(BaseModel):
    task_id: str
    platform: str
    verify_code: str


@router.post("/sms-login/start", summary="启动短信验证码登录（第一步：发送验证码）")
async def sms_login_start(
    request: SmsStartRequest,
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    短信验证码登录第一步：
    1. 启动浏览器打开登录页
    2. 自动填入手机号
    3. 点击"发送验证码"
    4. 返回 task_id，前端保存后用于第二步提交验证码

    当前支持：抖音来客（douyin）
    """
    result = await sms_login_service.start_sms_login(request.platform, request.phone)
    if result.get("success"):
        return success(data=result, message="验证码已发送，请查看手机")
    return error(message=result.get("error", "启动失败"))


@router.post("/sms-login/verify", summary="提交短信验证码（第二步：完成登录）")
async def sms_login_verify(
    request: SmsVerifyRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    短信验证码登录第二步：
    1. 在浏览器中填入验证码
    2. 点击登录按钮
    3. 等待登录成功
    4. 导出 storage_state 并保存到数据库

    成功后自动创建/更新 PlatformAccount。
    """
    result = await sms_login_service.verify_sms_code(
        task_id=request.task_id,
        platform=request.platform,
        verify_code=request.verify_code,
    )

    if result.get("status") == "success":
        platform_service = PlatformService(db)
        cookies = result["cookies"]
        platform = result["platform"]

        encrypted = await platform_service._encrypt_credentials({
            "username": "",
            "cookies": cookies,
        })

        # 查找已有账号或创建新账号
        stmt = select(PlatformAccount).where(
            PlatformAccount.user_id == current_user.id,
            PlatformAccount.platform == platform,
        )
        db_result = await db.execute(stmt)
        existing = db_result.scalar_one_or_none()

        if existing:
            existing.cookies_encrypted = encrypted
            existing.cookies_status = "valid"
            existing.last_sync_at = datetime.utcnow()
            existing.error_msg = None
        else:
            new_account = PlatformAccount(
                user_id=current_user.id,
                platform=platform,
                platform_username="",
                cookies_encrypted=encrypted,
                cookies_status="valid",
                last_sync_at=datetime.utcnow(),
            )
            db.add(new_account)

        await db.commit()

        return success(
            data={"status": "success", "platform": platform},
            message="登录成功，账号已绑定",
        )

    return error(message=result.get("error", "验证码登录失败"))


@router.post("/sms-login/cancel", summary="取消短信验证码登录")
async def sms_login_cancel(
    task_id: str = None,
) -> dict:
    """取消短信验证码登录流程"""
    if not task_id:
        return error(message="缺少 task_id")
    result = await sms_login_service.cancel_sms_login(task_id)
    return success(message="已取消" if result.get("success") else "取消失败")


@router.post("/accounts/{platform}/validate", summary="验证平台账号登录状态")
async def validate_platform_account(
    platform: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    验证指定平台的登录态是否仍然有效。

    流程：
    1. 从数据库读取该用户的平台账号 cookies_encrypted
    2. 解密获得 storage_state
    3. 用 Playwright 创建新 context 并访问平台页面
    4. 检测会话是否过期，更新 cookies_status
    """
    # 查找该用户的平台账号
    stmt = select(PlatformAccount).where(
        PlatformAccount.user_id == current_user.id,
        PlatformAccount.platform == platform,
    )
    result = await db.execute(stmt)
    account = result.scalar_one_or_none()

    if not account:
        return error(message=f"未找到 {platform} 平台绑定账号，请先扫码登录绑定")

    if not account.cookies_encrypted:
        return error(message="账号凭证为空，请重新扫码登录")

    # 解密凭证
    platform_service = PlatformService(db)
    credentials = await platform_service._decrypt_credentials(account.cookies_encrypted)

    # 从凭证中提取 storage_state
    storage_state = credentials.get("cookies", {}).get("_storage_state")
    if not storage_state:
        return error(message="未找到有效的登录状态，请重新扫码登录")

    # 调用验证服务
    from app.services.session_validation_service import SessionValidationService
    validate_service = SessionValidationService.get_instance()
    validate_result = await validate_service.validate(platform, storage_state)

    if validate_result.get("valid"):
        # 会话有效 —— 更新数据库状态
        account.cookies_status = "valid"
        account.error_msg = None

        # 如果返回了新的 storage_state，更新保存的凭证
        new_storage_state = validate_result.get("storage_state")
        if new_storage_state:
            credentials["cookies"]["_storage_state"] = new_storage_state
            account.cookies_encrypted = await platform_service._encrypt_credentials(credentials)

        # 更新用户名（如果提取到了新的）
        new_username = validate_result.get("username")
        if new_username:
            account.platform_username = new_username

        account.last_sync_at = datetime.utcnow()
        await db.commit()

        return success(
            data={
                "valid": True,
                "platform": platform,
                "platform_username": account.platform_username,
                "last_sync_at": account.last_sync_at.isoformat() if account.last_sync_at else None,
            },
            message="登录状态有效",
        )
    else:
        # 会话过期
        account.cookies_status = "expired"
        account.error_msg = validate_result.get("error", "会话验证失败")
        await db.commit()

        return error(
            data={
                "valid": False,
                "platform": platform,
                "error": validate_result.get("error"),
            },
            message="登录状态已过期，请重新扫码登录",
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
    from sqlalchemy import func

    # 主查询
    stmt = (
        select(PlatformAccount)
        .options(selectinload(PlatformAccount.user))
        .order_by(PlatformAccount.created_at.desc())
    )
    result = await db.execute(stmt)
    accounts = result.scalars().all()

    # 批量查询每个 account 下的 store_platforms 数量
    account_ids = [acc.id for acc in accounts]
    store_count_stmt = (
        select(
            StorePlatform.account_id,
            func.count(StorePlatform.id).label("store_count"),
        )
        .where(StorePlatform.account_id.in_(account_ids))
        .group_by(StorePlatform.account_id)
    )
    count_result = await db.execute(store_count_stmt)
    count_map = {row.account_id: row.store_count for row in count_result.all()}

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
            "platform_account_id": acc.platform_account_id or "",
            "cookies_status": acc.cookies_status or "unknown",
            "stores_count": count_map.get(acc.id, 0),
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
