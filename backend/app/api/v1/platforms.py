"""
平台关联路由模块
处理平台账号连接、店铺绑定、数据同步等平台关联相关接口
"""

from datetime import datetime
import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.deps import require_valid_subscription, get_db, require_roles
from app.core.response import success, error, paginated
from app.core.exceptions import NotFoundException
from app.models.user import User
from app.models.store import PlatformAccount, StorePlatform
from app.services.store_name_utils import find_best_matching_store_from_list
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


# ═══════════════════════════════════════════════════════
# 店铺同步辅助函数
# ═══════════════════════════════════════════════════════

async def _update_store_name_and_count(db: AsyncSession, StoreModel, store_id, ps_name: str):
    """更新系统门店名（取更长的）并递增 platform_count"""
    update_stmt = select(StoreModel).where(StoreModel.id == store_id)
    update_result = await db.execute(update_stmt)
    store_obj = update_result.scalar_one_or_none()
    if store_obj:
        if len(ps_name.strip()) > len(store_obj.name.strip()):
            old_name = store_obj.name
            store_obj.name = ps_name.strip()
            logger.info(f"[SyncAccount] Store name updated: '{old_name}' → '{ps_name.strip()}'")
        store_obj.platform_count = (store_obj.platform_count or 0) + 1


async def _create_new_store(db: AsyncSession, StoreModel, UserStore, user_id, name: str):
    """创建系统门店 + UserStore 关联，返回新门店对象（已 flush）"""
    new_store = StoreModel(
        name=name,
        type="restaurant",
        status="active",
        platform_count=1,
        owner_id=user_id,
    )
    db.add(new_store)
    await db.flush()

    user_store = UserStore(user_id=str(user_id), store_id=str(new_store.id))
    db.add(user_store)
    await db.flush()

    return new_store


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
    final_system_store_count = 0

    # 美团开店宝后台同时管理美团和大众点评两个平台
    # 同一个 poiId 在两个平台有各自的评论流（queryMTFeedbackPCNew / queryDPFeedbackPCNew）
    # 所以对 meituan 账号，每个店铺需要同时写入 meituan + dianping 两条 store_platforms 记录
    platforms_to_register = [platform]
    if platform == "meituan":
        platforms_to_register = ["meituan", "dianping"]

    if sync_result.get("status") == "success" and sync_result.get("stores"):
        stores = sync_result["stores"]
        from sqlalchemy import select
        from app.models.store import StorePlatform, Store as StoreModel
        from app.models.user import UserStore

        logger.info(f"[SyncAccount] sync_stores returned {len(stores)} stores, method={sync_result.get('method')}, targets={platforms_to_register}")

        # ═══════════════════════════════════════════════
        # 预查询: 一次性加载当前用户的所有系统门店（避免循环内重复查询）
        # 后续新建的门店直接追加到此列表，保持缓存同步
        # ═══════════════════════════════════════════════
        all_stores_stmt = select(StoreModel.id, StoreModel.name).join(
            UserStore, UserStore.store_id == StoreModel.id
        ).where(
            UserStore.user_id == str(current_user.id),
        )
        all_stores_result = await db.execute(all_stores_stmt)
        all_stores_cache = [{"id": row[0], "name": row[1]} for row in all_stores_result.all()]
        logger.info(f"[SyncAccount] Pre-loaded {len(all_stores_cache)} existing system stores for user {current_user.id}")

        for idx, store_info in enumerate(stores, 1):
            ps_id = store_info["platform_store_id"]
            ps_name = store_info["platform_store_name"]
            logger.info(f"[SyncAccount] ===== [{idx}/{len(stores)}] ps_id={ps_id}, ps_name='{ps_name}' =====")

            # 对需要同时注册的每个平台，分别创建/更新 store_platforms 记录
            for target_platform in platforms_to_register:

                # ── Step 1: 查找是否已存在 store_platform 记录 ──
                stmt = select(StorePlatform).where(
                    StorePlatform.account_id == account.id,
                    StorePlatform.platform_store_id == ps_id,
                    StorePlatform.platform == target_platform,
                )
                existing_result = await db.execute(stmt)
                existing_sp = existing_result.scalar_one_or_none()

                if existing_sp:
                    # ─── 已有 SP 记录：更新名称 ───
                    existing_sp.platform_store_name = ps_name
                    existing_sp.last_sync_at = datetime.utcnow()

                    if not existing_sp.store_id:
                        # 用本地缓存做相似度匹配
                        matched_id, sim_score, matched_name = find_best_matching_store_from_list(ps_name, all_stores_cache, threshold=0.9)

                        if matched_id:
                            existing_sp.store_id = str(matched_id)
                            existing_sp.connected = True
                            _update_store_name_and_count(db, StoreModel, matched_id, ps_name)
                            logger.info(f"[SyncAccount] [{target_platform}] Existing SP → bound to similar '{matched_name}' (sim={sim_score:.3f})")
                        else:
                            # 创建新门店
                            new_store = await _create_new_store(db, StoreModel, UserStore, current_user.id, ps_name)
                            existing_sp.store_id = new_store.id
                            existing_sp.connected = True
                            all_stores_cache.append({"id": new_store.id, "name": ps_name})
                            logger.info(f"[SyncAccount] [{target_platform}] Existing SP → created new store '{ps_name}' (id={new_store.id})")
                    else:
                        logger.info(f"[SyncAccount] [{target_platform}] Existing SP already bound to store_id={existing_sp.store_id}")
                else:
                    # ─── 新 SP 记录 ───
                    # Step 2: 查找同 poiId 其他平台的 SP 是否已关联门店
                    shared_stmt = select(StorePlatform.store_id).where(
                        StorePlatform.account_id == account.id,
                        StorePlatform.platform_store_id == ps_id,
                        StorePlatform.store_id.isnot(None),
                    ).limit(1)
                    shared_result = await db.execute(shared_stmt)
                    existing_store_id = shared_result.scalar_one_or_none()

                    if existing_store_id:
                        # 复用同 poiId 已有关联的门店
                        new_sp = StorePlatform(
                            account_id=account.id, platform=target_platform,
                            platform_store_id=ps_id, platform_store_name=ps_name,
                            store_id=str(existing_store_id), connected=True,
                            last_sync_at=datetime.utcnow(), sync_status="synced",
                        )
                        db.add(new_sp)
                        await db.flush()  # flush 以便后续 shared_stmt 查询能找到
                        _update_store_name_and_count(db, StoreModel, existing_store_id, ps_name)
                        logger.info(f"[SyncAccount] [{target_platform}] New SP → reused shared store_id={existing_store_id} (same poiId)")
                    else:
                        # Step 3: 用本地缓存做相似度匹配
                        matched_id, sim_score, matched_name = find_best_matching_store_from_list(ps_name, all_stores_cache, threshold=0.9)

                        if matched_id:
                            new_sp = StorePlatform(
                                account_id=account.id, platform=target_platform,
                                platform_store_id=ps_id, platform_store_name=ps_name,
                                store_id=str(matched_id), connected=True,
                                last_sync_at=datetime.utcnow(), sync_status="synced",
                            )
                            db.add(new_sp)
                            await db.flush()
                            _update_store_name_and_count(db, StoreModel, matched_id, ps_name)
                            logger.info(f"[SyncAccount] [{target_platform}] New SP → matched '{matched_name}' (sim={sim_score:.3f})")
                        else:
                            # Step 4: 创建全新门店
                            logger.info(f"[SyncAccount] [{target_platform}] No match in {len(all_stores_cache)} stores, creating new '{ps_name}'")
                            new_store = await _create_new_store(db, StoreModel, UserStore, current_user.id, ps_name.strip())
                            new_sp = StorePlatform(
                                account_id=account.id, platform=target_platform,
                                platform_store_id=ps_id, platform_store_name=ps_name,
                                store_id=new_store.id, connected=True,
                                last_sync_at=datetime.utcnow(), sync_status="synced",
                            )
                            db.add(new_sp)
                            await db.flush()
                            all_stores_cache.append({"id": new_store.id, "name": ps_name.strip()})
                            logger.info(f"[SyncAccount] [{target_platform}] ✓ Created '{ps_name}' (id={new_store.id}), cache={len(all_stores_cache)} stores")
            synced_stores += 1

        # 记录最终系统门店缓存大小
        final_system_store_count = len(all_stores_cache)

    # 更新同步时间
    account.last_sync_at = datetime.utcnow()
    await db.commit()

    # 输出最终统计
    logger.info(f"[SyncAccount] ═══ Sync complete: {synced_stores} platform stores, {final_system_store_count} system stores ═══")

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


@router.post("/accounts/{account_id}/sync-reviews", summary="同步平台评论数据（异步）")
async def sync_account_reviews(
    account_id: UUID,
    sync_mode: str = Query("incremental", description="同步模式: full=全量(全部历史), incremental=增量(近30天)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    异步启动评论同步任务，立即返回 task_id。
    前端通过 GET /accounts/{account_id}/sync-reviews/status/{task_id} 轮询进度。
    同步完成后通过 GET /accounts/{account_id}/sync-reviews/result/{task_id} 获取结果。
    """
    from app.models.review import Review
    from app.services.review_sync_service import ReviewSyncService
    from app.services.platform_service import PlatformService

    platform_service = PlatformService(db)
    account = await platform_service.get_account_by_id(account_id)
    if not account or str(account.user_id) != str(current_user.id):
        raise NotFoundException("平台账号不存在")

    storage_state = await platform_service._decrypt_credentials(account.cookies_encrypted)
    if not storage_state or not storage_state.get("cookies"):
        return error(message="登录态解密失败或格式错误，请重新扫码登录")

    stmt = select(StorePlatform).where(
        StorePlatform.account_id == account.id,
        StorePlatform.store_id.isnot(None),
    )
    result = await db.execute(stmt)
    store_platforms = result.scalars().all()

    if not store_platforms:
        return error(message="暂无已绑定的店铺，请先同步店铺列表")

    # 按 platform 分组店铺
    stores_by_platform: dict[str, list] = {}
    for sp in store_platforms:
        if not sp.platform_store_id:
            continue
        store_info = {
            "platform_store_id": sp.platform_store_id,
            "platform_store_name": sp.platform_store_name,
            "store_id": str(sp.store_id) if sp.store_id else "",
        }
        # 抖音需要 life_account_id（即平台账号ID）
        if sp.platform == "douyin" and account.platform_account_id:
            store_info["account_id"] = account.platform_account_id
        stores_by_platform.setdefault(sp.platform, []).append(store_info)

    review_service = ReviewSyncService.get_instance()
    time_type = "全部" if sync_mode == "full" else "近30天"
    task_id = await review_service.start_sync_reviews_async(
        account_id=str(account_id),
        storage_state=storage_state,
        stores_by_platform=stores_by_platform,
        time_type=time_type,
    )

    return success(
        data={
            "task_id": task_id,
            "platforms": list(stores_by_platform.keys()),
            "store_count": len(store_platforms),
            "sync_mode": sync_mode,
        },
        message=f"{'全量' if sync_mode == 'full' else '增量'}评论同步任务已启动",
    )


@router.get("/accounts/{account_id}/sync-reviews/status/{task_id}", summary="查询评论同步进度")
async def get_sync_reviews_status(
    account_id: UUID,
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    查询评论同步任务状态（前端轮询）。
    - running: 同步中（含 current_platform, progress）
    - success: 同步完成，调用 /result/{task_id} 入库
    - failed: 同步失败（含 error 信息）
    """
    from app.services.review_sync_service import ReviewSyncService

    review_service = ReviewSyncService.get_instance()
    status = review_service.get_sync_reviews_status(task_id)

    if status["status"] == "not_found":
        return error(message="同步任务不存在或已过期")

    return success(data=status)


@router.get("/accounts/{account_id}/sync-reviews/result/{task_id}", summary="获取评论同步结果")
async def get_sync_reviews_result(
    account_id: UUID,
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取评论同步结果（入库已在后台完成，此接口只返回统计数字）。
    """
    from app.services.review_sync_service import ReviewSyncService

    review_service = ReviewSyncService.get_instance()
    status = review_service.get_sync_reviews_status(task_id)

    if status["status"] == "not_found":
        return error(message="同步任务不存在或已过期")
    if status["status"] == "running":
        return error(message="同步尚未完成")
    if status["status"] == "failed":
        return error(message=f"同步失败: {status.get('error', '未知错误')}")

    result_data = status.get("result", {})
    created = result_data.get("created", 0)
    skipped = result_data.get("skipped", 0)
    errors = result_data.get("errors", [])

    return success(
        data={
            "created": created,
            "skipped": skipped,
            "total": result_data.get("review_count", 0),
            "errors": errors,
        },
        message=f"评论同步完成，新增 {created} 条，跳过 {skipped} 条重复",
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
        platform_username = result.get("platform_username", "")
        platform_account_id = result.get("platform_account_id", "")
        platform_phone = result.get("platform_phone", "")
        platform_role = result.get("platform_role", "")

        logger.info(f"[SMS Verify] Saving account: username={platform_username}, account_id={platform_account_id}, phone={platform_phone}, role={platform_role}")

        encrypted = await platform_service._encrypt_credentials({
            "username": platform_username,
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
            existing.platform_username = platform_username or existing.platform_username
            existing.platform_account_id = platform_account_id or existing.platform_account_id
            existing.last_sync_at = datetime.utcnow()
            existing.error_msg = None
        else:
            new_account = PlatformAccount(
                user_id=current_user.id,
                platform=platform,
                platform_username=platform_username or "未知用户",
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
                "platform_account_id": platform_account_id,
                "platform_phone": platform_phone,
                "platform_role": platform_role,
            },
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
