"""
门店服务模块
处理门店的增删改查、统计、权限过滤等业务逻辑
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, ForbiddenException, NotFoundException
from app.models.review import Review
from app.models.store import Store, StorePlatform
from app.models.user import User, UserStore
from app.services import user_region_service  # 导入用户区域服务


async def _build_store_filter_for_user(query, user: User, db: AsyncSession):
    """
    根据用户角色和区域权限构建门店过滤条件。
    权限计算：取并集（区域权限 + 直接店铺权限）。
    预查询 user_stores 获取 ID 列表，避免子查询可能引发的 SAWarning。
    """

    # 超级管理员不受限制
    if user.role in ["SUPER_ADMIN", "HQ"]:
        return query

    # 获取用户关联的区域（包括子级）
    region_ids = await user_region_service.get_user_accessible_region_ids(db, user.id)

    # 预查询用户直接关联的门店 ID（避免子查询）
    user_store_result = await db.execute(
        select(UserStore.store_id).where(UserStore.user_id == user.id)
    )
    owned_store_ids = [row[0] for row in user_store_result.all()]

    # 构建过滤条件：店铺的 region_id 在用户区域内 OR 店铺直接关联用户
    if region_ids:
        # 区域权限：店铺的 region_id 在用户可访问的区域列表中
        region_filter = Store.region_id.in_(region_ids)

        # 直接关联权限：通过 owner_id 或 user_stores 预查询结果
        if owned_store_ids:
            direct_filter = or_(
                Store.owner_id == user.id,
                Store.id.in_(owned_store_ids),
            )
        else:
            direct_filter = Store.owner_id == user.id

        # 取并集
        return query.where(or_(region_filter, direct_filter))
    else:
        # 如果没有区域权限，只能看直接关联的店铺
        if owned_store_ids:
            return query.where(
                or_(
                    Store.owner_id == user.id,
                    Store.id.in_(owned_store_ids),
                )
            )
        else:
            return query.where(Store.owner_id == user.id)


async def get_stores(
    db: AsyncSession,
    user: User,
    page: int = 1,
    page_size: int = 20,
    type: Optional[str] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
) -> tuple[list[Store], int]:
    """
    获取门店列表（支持筛选、分页、角色过滤）

    Args:
        db: 数据库会话
        user: 当前用户
        page: 页码
        page_size: 每页数量
        type: 门店类型筛选
        status: 门店状态筛选
        keyword: 关键词搜索（名称/地址）

    Returns:
        tuple[list[Store], int]: (门店列表, 总数)
    """
    # 构建基础查询
    query = select(Store)
    count_query = select(func.count(Store.id))

    # 角色过滤 - 需要使用 await
    query = await _build_store_filter_for_user(query, user, db)
    count_query = await _build_store_filter_for_user(count_query, user, db)

    # 条件筛选
    conditions = []
    if type:
        conditions.append(Store.type == type)
    if status:
        conditions.append(Store.status == status)
    if keyword:
        conditions.append(
            or_(
                Store.name.ilike(f"%{keyword}%"),
                Store.address.ilike(f"%{keyword}%"),
            )
        )

    for cond in conditions:
        query = query.where(cond)
        count_query = count_query.where(cond)

    # 查询总数
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(Store.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    stores = list(result.scalars().all())

    return stores, total


async def get_store_by_id(
    db: AsyncSession,
    store_id: UUID,
) -> Store:
    """
    根据ID获取门店详情

    Args:
        db: 数据库会话
        store_id: 门店ID

    Returns:
        Store: 门店对象

    Raises:
        NotFoundException: 门店不存在
    """
    result = await db.execute(
        select(Store).where(Store.id == store_id)
    )
    store = result.scalar_one_or_none()
    if not store:
        raise NotFoundException("门店不存在")
    return store


async def create_store(
    db: AsyncSession,
    store_data: dict,
) -> Store:
    """
    创建门店
    如果指定了 owner_id，自动在 user_stores 表创建关联记录

    Args:
        db: 数据库会话
        store_data: 门店数据字典

    Returns:
        Store: 创建的门店对象
    """
    owner_id = store_data.get("owner_id")
    store = Store(**{k: v for k, v in store_data.items() if k != "owner_id"})
    db.add(store)
    await db.flush()

    # 同步 owner_id 到 user_stores 表
    if owner_id:
        existing = await db.execute(
            select(UserStore).where(
                UserStore.user_id == owner_id,
                UserStore.store_id == store.id,
            )
        )
        if not existing.scalar_one_or_none():
            db.add(UserStore(user_id=owner_id, store_id=store.id))

    await db.refresh(store)
    return store


async def update_store(
    db: AsyncSession,
    store_id: UUID,
    store_data: dict,
) -> Store:
    """
    更新门店信息
    如果 owner_id 发生变化，同步更新 user_stores 表

    Args:
        db: 数据库会话
        store_id: 门店ID
        store_data: 更新数据字典

    Returns:
        Store: 更新后的门店对象

    Raises:
        NotFoundException: 门店不存在
    """
    store = await get_store_by_id(db, store_id)

    new_owner_id = store_data.get("owner_id")
    old_owner_id = store.owner_id

    for key, value in store_data.items():
        if value is not None and hasattr(store, key):
            setattr(store, key, value)

    # 同步 owner_id 变更到 user_stores 表
    if "owner_id" in store_data and new_owner_id != old_owner_id:
        # 删除旧的关联（如果存在）
        if old_owner_id:
            await db.execute(
                UserStore.__table__.delete().where(
                    UserStore.user_id == old_owner_id,
                    UserStore.store_id == store_id,
                )
            )
        # 创建新的关联
        if new_owner_id:
            existing = await db.execute(
                select(UserStore).where(
                    UserStore.user_id == new_owner_id,
                    UserStore.store_id == store_id,
                )
            )
            if not existing.scalar_one_or_none():
                db.add(UserStore(user_id=new_owner_id, store_id=store_id))

    await db.flush()
    await db.refresh(store)
    return store


async def delete_store(
    db: AsyncSession,
    store_id: UUID,
) -> None:
    """
    删除门店

    Args:
        db: 数据库会话
        store_id: 门店ID

    Raises:
        NotFoundException: 门店不存在
    """
    store = await get_store_by_id(db, store_id)
    await db.delete(store)
    await db.flush()


async def activate_store(
    db: AsyncSession,
    store_id: UUID,
) -> Store:
    """
    激活门店（将状态设为 active）

    Args:
        db: 数据库会话
        store_id: 门店ID

    Returns:
        Store: 更新后的门店对象

    Raises:
        NotFoundException: 门店不存在
        BusinessException: 门店已激活
    """
    store = await get_store_by_id(db, store_id)
    if store.status == "active":
        raise BusinessException("门店已处于激活状态")

    store.status = "active"
    await db.flush()
    await db.refresh(store)
    return store


async def get_store_review_stats(
    db: AsyncSession,
    store_id: UUID,
    period: Optional[str] = None,
) -> dict:
    """
    获取门店评价统计

    Args:
        db: 数据库会话
        store_id: 门店ID
        period: 统计周期 (7d/30d/90d/all)，默认 all

    Returns:
        dict: 评价统计数据
    """
    store = await get_store_by_id(db, store_id)

    # 构建基础查询
    query = select(Review).where(
        Review.store_id == store_id,
        Review.status == "normal",
    )

    # 按周期过滤
    if period and period != "all":
        try:
            days = int(period.replace("d", ""))
            from datetime import timedelta

            since = datetime.now() - timedelta(days=days)
            query = query.where(Review.created_at >= since)
        except ValueError:
            pass

    result = await db.execute(query)
    reviews = list(result.scalars().all())

    total = len(reviews)
    if total == 0:
        return {
            "total_reviews": 0,
            "avg_rating": 0.0,
            "positive_rate": 0.0,
            "negative_rate": 0.0,
            "reply_rate": 0.0,
            "sentiment_distribution": {},
        }

    # 计算统计数据
    avg_rating = sum(r.rating for r in reviews) / total
    replied = sum(1 for r in reviews if r.reply)
    reply_rate = replied / total * 100

    positive = sum(1 for r in reviews if r.sentiment == "positive")
    negative = sum(1 for r in reviews if r.sentiment == "negative")
    neutral = sum(1 for r in reviews if r.sentiment == "neutral")

    sentiment_distribution = {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
    }

    positive_rate = positive / total * 100
    negative_rate = negative / total * 100

    return {
        "total_reviews": total,
        "avg_rating": round(avg_rating, 1),
        "positive_rate": round(positive_rate, 1),
        "negative_rate": round(negative_rate, 1),
        "reply_rate": round(reply_rate, 1),
        "sentiment_distribution": sentiment_distribution,
    }


async def get_store_monthly_stats(
    db: AsyncSession,
    store_id: UUID,
) -> list[dict]:
    """
    获取门店月度统计（最近12个月）

    Args:
        db: 数据库会话
        store_id: 门店ID

    Returns:
        list[dict]: 月度统计数据列表
    """
    # 确保门店存在
    await get_store_by_id(db, store_id)

    # 查询最近12个月的评论
    from datetime import timedelta

    since = datetime.now() - timedelta(days=365)
    result = await db.execute(
        select(Review).where(
            Review.store_id == store_id,
            Review.status == "normal",
            Review.created_at >= since,
        )
    )
    reviews = list(result.scalars().all())

    # 按月分组统计
    monthly_data: dict[str, dict] = {}
    for review in reviews:
        month_key = review.created_at.strftime("%Y-%m")
        if month_key not in monthly_data:
            monthly_data[month_key] = {
                "month": month_key,
                "total_reviews": 0,
                "avg_rating": 0.0,
                "positive_count": 0,
                "negative_count": 0,
                "reply_count": 0,
                "_rating_sum": 0,
            }
        stats = monthly_data[month_key]
        stats["total_reviews"] += 1
        stats["_rating_sum"] += review.rating
        if review.sentiment == "positive":
            stats["positive_count"] += 1
        elif review.sentiment == "negative":
            stats["negative_count"] += 1
        if review.reply:
            stats["reply_count"] += 1

    # 计算平均评分并清理内部字段
    result_list = []
    for stats in monthly_data.values():
        if stats["total_reviews"] > 0:
            stats["avg_rating"] = round(
                stats["_rating_sum"] / stats["total_reviews"], 1
            )
        del stats["_rating_sum"]
        result_list.append(stats)

    # 按月份倒序排列
    result_list.sort(key=lambda x: x["month"], reverse=True)
    return result_list


async def get_store_recent_reviews(
    db: AsyncSession,
    store_id: UUID,
    limit: int = 10,
) -> list[Review]:
    """
    获取门店最近评论

    Args:
        db: 数据库会话
        store_id: 门店ID
        limit: 返回数量

    Returns:
        list[Review]: 评论列表
    """
    # 确保门店存在
    await get_store_by_id(db, store_id)

    result = await db.execute(
        select(Review)
        .where(Review.store_id == store_id, Review.status == "normal")
        .order_by(Review.created_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_stores_stats(
    db: AsyncSession,
    user: User,
) -> dict:
    """
    获取用户可访问门店的汇总统计

    Args:
        db: 数据库会话
        user: 当前用户

    Returns:
        dict: 汇总统计数据
    """
    # 构建基础查询
    query = select(Store)
    query = await _build_store_filter_for_user(query, user, db)

    result = await db.execute(query)
    stores = list(result.scalars().all())

    total_stores = len(stores)
    active_stores = sum(1 for s in stores if s.status == "active")
    pending_stores = sum(1 for s in stores if s.status == "pending")
    inactive_stores = sum(1 for s in stores if s.status == "inactive")
    total_reviews = sum(s.review_count for s in stores)

    # 按类型统计
    type_distribution: dict[str, int] = {}
    for store in stores:
        type_distribution[store.type] = type_distribution.get(store.type, 0) + 1

    return {
        "total_stores": total_stores,
        "active_stores": active_stores,
        "pending_stores": pending_stores,
        "inactive_stores": inactive_stores,
        "total_reviews": total_reviews,
        "type_distribution": type_distribution,
    }
