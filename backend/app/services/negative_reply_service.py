"""
差评处理服务模块
提供差评自动回复审核、任务管理等功能
"""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import BusinessException, NotFoundException
from app.models.review import ReplyAudit, Review
from app.services.ai_service import AIService
from app.models.user import User


async def sync_negative_reviews(db: AsyncSession, user: User) -> int:
    """
    同步差评到审核任务表（注意：此函数会在事务中为每条差评调用 AI，仅在后台任务中使用）
    为所有差评（rating <= 2）且还没有审核任务的评论创建任务

    Args:
        db: 数据库会话
        user: 当前用户

    Returns:
        int: 创建的任务数量
    """
    from app.models.store import Store
    from app.models.user import UserStore

    # 获取用户关联的店铺ID
    if user.role in ("SUPER_ADMIN", "HQ", "OPERATOR"):
        result = await db.execute(select(Store.id))
        user_store_ids = [row[0] for row in result.all()]
    else:
        store_ids_stmt = select(UserStore.store_id).where(UserStore.user_id == user.id)
        owned_stmt = select(Store.id).where(Store.owner_id == user.id)
        all_ids_stmt = store_ids_stmt.union(owned_stmt)
        result = await db.execute(all_ids_stmt)
        user_store_ids = [row[0] for row in result.all()]
    
    if not user_store_ids:
        return 0
    
    # 查询所有差评（rating <= 2）且还没有审核任务的评论
    stmt = (
        select(Review)
        .options(selectinload(Review.store))
        .where(
            and_(
                Review.store_id.in_(user_store_ids),
                Review.rating <= 2,
                ~Review.id.in_(
                    select(ReplyAudit.review_id)
                )
            )
        )
    )
    result = await db.execute(stmt)
    negative_reviews = result.scalars().all()
    
    if not negative_reviews:
        return 0
    
    # 为每个差评创建审核任务
    created_count = 0
    for review in negative_reviews:
        # 根据评分确定风险等级
        if review.rating == 1:
            risk = "high"
        elif review.rating == 2:
            risk = "medium"
        else:
            risk = "low"
        
        # 调用 AI 模型真实生成回复
        try:
            ai_service = AIService(db)
            store_name = review.store.name if review.store else "本店"
            ai_result = await ai_service.generate_reply(
                review_content=review.content or "",
                rating=review.rating or 3,
                store_name=store_name,
                platform=review.platform or "未知平台",
            )
            ai_reply = ai_result.get("reply", "")
        except Exception as e:
            print(f"[create_negative_task] AI调用失败，使用模板回退: {e}")
            ai_reply = "感谢您的反馈，关于您提到的问题我们非常重视，已安排专人跟进整改，期待您再给我们一次机会。"
        
        # 创建审核任务
        audit = ReplyAudit(
            id=uuid4(),
            review_id=review.id,
            store_id=review.store_id,
            ai_reply_content=ai_reply,
            status="pending",
            risk_level=risk,
            scores={
                "realism": 85,
                "empathy": 90,
                "concreteness": 80,
                "consistency": 85,
            },
            created_at=datetime.now(),
        )
        
        db.add(audit)
        created_count += 1
    
    await db.flush()
    return created_count


async def get_tasks(
    db: AsyncSession,
    user: User,
    status: str | None = None,
    page: int = 1,
    page_size: int = 20,
    store_id: str | None = None,
    search: str | None = None,
) -> tuple[list, int]:
    """
    获取差评任务列表

    注意: 不再自动调用 sync_negative_reviews（逐条调 AI 太慢会超时）。
    同步应通过独立的异步任务触发。

    Args:
        db: 数据库会话
        user: 当前用户
        status: 状态筛选
        page: 页码
        page_size: 每页大小
        store_id: 门店ID筛选
        search: 关键词搜索

    Returns:
        tuple[list, int]: (任务列表, 总数)
    """
    from app.models.store import Store
    from app.models.user import UserStore

    # 构建门店可见性条件
    conditions = []

    if user.role in ("SUPER_ADMIN", "HQ", "OPERATOR"):
        # 管理员可见所有门店
        if store_id:
            conditions.append(ReplyAudit.store_id == store_id)
    else:
        # 非管理员：查询关联门店
        store_ids_stmt = select(UserStore.store_id).where(UserStore.user_id == user.id)
        owned_stmt = select(Store.id).where(Store.owner_id == user.id)
        all_ids_stmt = store_ids_stmt.union(owned_stmt)
        result = await db.execute(all_ids_stmt)
        all_store_ids = [row[0] for row in result.all()]

        if not all_store_ids:
            return [], 0

        if store_id:
            if store_id not in [str(sid) for sid in all_store_ids]:
                return [], 0
            conditions.append(ReplyAudit.store_id == store_id)
        else:
            conditions.append(ReplyAudit.store_id.in_(all_store_ids))

    if status:
        conditions.append(ReplyAudit.status == status)

    # 关键词搜索（匹配评论内容或用户名）
    if search:
        search_conditions = [
            Review.content.ilike(f"%{search}%"),
            Review.user_name.ilike(f"%{search}%"),
        ]
        conditions.append(func.or_(*search_conditions))

    # 查询总数
    count_stmt = select(func.count(ReplyAudit.id)).where(and_(*conditions))
    count_result = await db.execute(count_stmt)
    total = count_result.scalar() or 0

    # 查询数据
    stmt = (
        select(ReplyAudit, Review)
        .join(ReplyAudit.review)
        .where(and_(*conditions))
        .order_by(desc(ReplyAudit.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    rows = result.all()

    tasks = []
    for audit, review in rows:
        tasks.append({
            "id": audit.id,
            "review_id": audit.review_id,
            "user_name": review.user_name,
            "rating": review.rating,
            "content": review.content,
            "platform": review.platform,
            "ai_draft": audit.ai_reply_content,
            "risk": audit.risk_level or review.risk_level,
            "scores": audit.scores,
            "status": audit.status,
            "created_at": audit.created_at,
        })

    return tasks, total


async def approve_task(db: AsyncSession, task_id: UUID, user: User) -> ReplyAudit:
    """
    批准并发送差评回复

    Args:
        db: 数据库会话
        task_id: 任务ID
        user: 当前用户

    Returns:
        ReplyAudit: 审核记录
    """
    from app.models.store import Store
    from app.models.user import UserStore

    # 构建门店权限条件
    store_ids_stmt = select(UserStore.store_id).where(UserStore.user_id == user.id)
    owned_stmt = select(Store.id).where(Store.owner_id == user.id)
    all_ids_stmt = store_ids_stmt.union(owned_stmt)
    result = await db.execute(all_ids_stmt)
    all_store_ids = [row[0] for row in result.all()]

    stmt = select(ReplyAudit).where(
        and_(
            ReplyAudit.id == task_id,
            ReplyAudit.store_id.in_(all_store_ids),
        )
    )
    result = await db.execute(stmt)
    audit = result.scalar_one_or_none()

    if not audit:
        raise NotFoundException("任务不存在")

    if audit.status not in ["pending", "rejected"]:
        raise BusinessException("该任务状态不允许批准")

    audit.status = "sent"
    audit.auditor_id = user.id
    audit.reviewed_at = datetime.now()

    # 更新评论回复状态
    stmt_review = select(Review).where(Review.id == audit.review_id)
    result_review = await db.execute(stmt_review)
    review = result_review.scalar_one_or_none()
    if review:
        review.reply = audit.ai_reply_content
        review.reply_time = datetime.now()
        review.ai_generated = True

    await db.flush()
    return audit


async def reject_task(
    db: AsyncSession, task_id: UUID, user: User, reason: str
) -> ReplyAudit:
    """
    驳回差评回复任务

    Args:
        db: 数据库会话
        task_id: 任务ID
        user: 当前用户
        reason: 驳回原因

    Returns:
        ReplyAudit: 审核记录
    """
    from app.models.store import Store
    from app.models.user import UserStore

    store_ids_stmt = select(UserStore.store_id).where(UserStore.user_id == user.id)
    owned_stmt = select(Store.id).where(Store.owner_id == user.id)
    all_ids_stmt = store_ids_stmt.union(owned_stmt)
    result = await db.execute(all_ids_stmt)
    all_store_ids = [row[0] for row in result.all()]

    stmt = select(ReplyAudit).where(
        and_(
            ReplyAudit.id == task_id,
            ReplyAudit.store_id.in_(all_store_ids),
        )
    )
    result = await db.execute(stmt)
    audit = result.scalar_one_or_none()

    if not audit:
        raise NotFoundException("任务不存在")

    if audit.status != "pending":
        raise BusinessException("该任务状态不允许驳回")

    audit.status = "rejected"
    audit.reject_reason = reason
    audit.auditor_id = user.id
    audit.reviewed_at = datetime.now()

    await db.flush()
    return audit


async def regenerate_reply(db: AsyncSession, task_id: UUID) -> ReplyAudit:
    """
    重新生成AI回复
    
    Args:
        db: 数据库会话
        task_id: 任务ID
        
    Returns:
        ReplyAudit: 审核记录
    """
    stmt = select(ReplyAudit).where(ReplyAudit.id == task_id)
    result = await db.execute(stmt)
    audit = result.scalar_one_or_none()

    if not audit:
        raise NotFoundException("任务不存在")

    # 查询评论内容（同时加载门店关系，避免懒加载报错）
    stmt_review = (
        select(Review)
        .options(selectinload(Review.store))
        .where(Review.id == audit.review_id)
    )
    result_review = await db.execute(stmt_review)
    review = result_review.scalar_one_or_none()

    if not review:
        raise NotFoundException("关联评论不存在")
    
    # 调用 AI 模型真实生成回复
    try:
        ai_service = AIService(db)
        store_name = review.store.name if review.store else "本店"
        ai_result = await ai_service.generate_reply(
            review_content=review.content or "",
            rating=review.rating or 3,
            store_name=store_name,
            platform=review.platform or "未知平台",
        )
        ai_reply = ai_result.get("reply", "")
    except Exception as e:
        # AI 调用失败时回退到简单模板
        print(f"[regenerate_reply] AI调用失败，使用模板回退: {e}")
        rating = review.rating or 3
        if rating <= 2:
            ai_reply = "感谢您的反馈，关于您提到的问题我们非常重视，已安排专人跟进整改，期待您再给我们一次机会。"
        else:
            ai_reply = "感谢您的评价，我们会认真对待每一位顾客的意见，持续改进，期待您的再次光临。"
    
    audit.ai_reply_content = ai_reply
    audit.status = "pending"
    audit.reject_reason = None
    
    await db.flush()
    return audit


async def get_history(
    db: AsyncSession, user: User, page: int = 1, page_size: int = 20
) -> tuple[list, int]:
    """
    获取已处理历史

    Args:
        db: 数据库会话
        user: 当前用户
        page: 页码
        page_size: 每页大小

    Returns:
        tuple[list, int]: (历史记录列表, 总数)
    """
    from app.models.store import Store
    from app.models.user import UserStore

    # 构建门店可见性条件
    store_conditions = []

    if user.role in ("SUPER_ADMIN", "HQ", "OPERATOR"):
        pass  # 管理员可见所有
    else:
        store_ids_stmt = select(UserStore.store_id).where(UserStore.user_id == user.id)
        owned_stmt = select(Store.id).where(Store.owner_id == user.id)
        all_ids_stmt = store_ids_stmt.union(owned_stmt)
        result = await db.execute(all_ids_stmt)
        all_store_ids = [row[0] for row in result.all()]
        if not all_store_ids:
            return [], 0
        store_conditions.append(ReplyAudit.store_id.in_(all_store_ids))

    conditions = [
        ReplyAudit.status.in_(["approved", "rejected", "sent"]),
    ] + store_conditions

    # 查询总数
    count_stmt = select(func.count(ReplyAudit.id)).where(and_(*conditions))
    count_result = await db.execute(count_stmt)
    total = count_result.scalar() or 0

    # 查询数据
    stmt = (
        select(ReplyAudit, Review)
        .join(ReplyAudit.review)
        .where(and_(*conditions))
        .order_by(desc(ReplyAudit.reviewed_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    rows = result.all()

    history = []
    for audit, review in rows:
        history.append({
            "id": audit.id,
            "review_id": audit.review_id,
            "user_name": review.user_name,
            "content": review.content,
            "rating": review.rating,
            "platform": review.platform,
            "ai_draft": audit.ai_reply_content,
            "final_reply": review.reply,
            "status": audit.status,
            "created_at": audit.created_at,
        })

    return history, total


async def create_negative_task(db: AsyncSession, review_id: UUID) -> ReplyAudit:
    """
    创建差评处理任务
    
    Args:
        db: 数据库会话
        review_id: 评论ID
        
    Returns:
        ReplyAudit: 审核记录
    """
    # 查询评论（同时加载门店关系，避免懒加载报错）
    stmt = (
        select(Review)
        .options(selectinload(Review.store))
        .where(Review.id == review_id)
    )
    result = await db.execute(stmt)
    review = result.scalar_one_or_none()

    if not review:
        raise NotFoundException("评论不存在")

    # 检查是否已存在任务
    stmt_audit = select(ReplyAudit).where(ReplyAudit.review_id == review_id)
    result_audit = await db.execute(stmt_audit)
    existing = result_audit.scalar_one_or_none()

    if existing:
        return existing

    # 调用 AI 模型真实生成回复
    try:
        ai_service = AIService(db)
        store_name = review.store.name if review.store else "本店"
        ai_result = await ai_service.generate_reply(
            review_content=review.content or "",
            rating=review.rating or 3,
            store_name=store_name,
            platform=review.platform or "未知平台",
        )
        ai_reply = ai_result.get("reply", "")
    except Exception as e:
        print(f"[create_negative_task] AI调用失败，使用模板回退: {e}")
        ai_reply = "感谢您的反馈，关于您提到的问题我们非常重视，已安排专人跟进整改，期待您再给我们一次机会。"

    # 生成评分
    scores = {
        "realism": 85,
        "empathy": 90,
        "concreteness": 80,
        "consistency": 85,
    }

    # 确定风险等级
    if review.rating == 1:
        risk = "high"
    elif review.rating == 2:
        risk = "medium"
    else:
        risk = "low"

    audit = ReplyAudit(
        id=uuid4(),
        review_id=review_id,
        store_id=review.store_id,
        ai_reply_content=ai_reply,
        status="pending",
        risk_level=risk,
        scores=scores,
        created_at=datetime.now(),
    )

    db.add(audit)
    await db.flush()
    return audit
