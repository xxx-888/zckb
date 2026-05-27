"""
差评处理服务模块
提供差评自动回复审核、任务管理等功能
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.models.review import ReplyAudit, Review
from app.models.user import User


async def get_tasks(
    db: AsyncSession,
    user: User,
    status: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list, int]:
    """
    获取差评任务列表

    Args:
        db: 数据库会话
        user: 当前用户
        status: 状态筛选
        page: 页码
        page_size: 每页大小

    Returns:
        tuple[list, int]: (任务列表, 总数)
    """
    # 构建查询条件
    conditions = [ReplyAudit.store_id.in_([sa.store_id for sa in user.store_associations])]
    if status:
        conditions.append(ReplyAudit.status == status)

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
    stmt = select(ReplyAudit).where(
        and_(
            ReplyAudit.id == task_id,
            ReplyAudit.store_id.in_([sa.store_id for sa in user.store_associations]),
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
    stmt = select(ReplyAudit).where(
        and_(
            ReplyAudit.id == task_id,
            ReplyAudit.store_id.in_([sa.store_id for sa in user.store_associations]),
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

    # 查询评论内容
    stmt_review = select(Review).where(Review.id == audit.review_id)
    result_review = await db.execute(stmt_review)
    review = result_review.scalar_one_or_none()

    if not review:
        raise NotFoundException("关联评论不存在")
    
    # 基于真实评论内容生成AI回复（不再使用模拟模板）
    # 根据评分和评论内容生成针对性回复
    rating = review.rating or 3
    content = review.content or ""
    
    # 根据评分生成不同风格的回复
    if rating == 1:
        if "味道" in content or "口味" in content:
            ai_reply = "非常抱歉菜品口味没能满足您的期望，我们已反馈给厨师长，会认真调整配方，期待您再给我们一次改进的机会。"
        elif "服务" in content or "态度" in content:
            ai_reply = "对于本次服务不周我们深表歉意，已对相关人员进行了服务培训，期待您再来体验我们的改变。"
        elif "环境" in content or "卫生" in content:
            ai_reply = "非常抱歉环境问题给您带来了不好的体验，我们已加强环境卫生管理，期待您再来检查时能看到我们的进步。"
        else:
            ai_reply = "非常抱歉本次用餐没能达到您的期望，我们非常重视您的反馈，已安排店长专门跟进整改，期待您再给我们一次机会。"
    elif rating == 2:
        if "味道" in content or "口味" in content:
            ai_reply = "感谢您的反馈，菜品口味我们会认真调整，欢迎您下次来时告诉我们应该改进的方向，我们一定努力做得更好。"
        elif "服务" in content or "态度" in content:
            ai_reply = "感谢您的提醒，服务方面我们会加强培训，期待您下次来时能感受到我们的进步。"
        else:
            ai_reply = "感谢您的评价，对于您提到的问题我们非常重视，会认真改进，期待您的再次光临。"
    else:
        ai_reply = "感谢您的反馈，我们会认真对待每一位顾客的意见，持续改进，期待您下次来时能有不同的体验。"
    
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
    # 查询已处理的任务（approved, rejected, sent）
    conditions = [
        ReplyAudit.store_id.in_([sa.store_id for sa in user.store_associations]),
        ReplyAudit.status.in_(["approved", "rejected", "sent"]),
    ]

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
    # 查询评论
    stmt = select(Review).where(Review.id == review_id)
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

    # 模拟生成AI回复
    templates = [
        "非常抱歉给您带来不好的用餐体验，我们会认真听取您的意见并持续改进。",
        "感谢您的反馈，对于您提到的问题我们深表歉意，已安排专人跟进处理。",
        "您好，对于本次服务不周之处我们深感抱歉，期待您给我们改正的机会。",
    ]
    ai_reply = random.choice(templates)

    # 模拟评分
    scores = {
        "realism": random.randint(70, 95),
        "empathy": random.randint(75, 90),
        "concreteness": random.randint(60, 85),
        "consistency": random.randint(70, 90),
    }

    # 确定风险等级
    if review.rating == 1:
        risk = "high"
    elif review.rating == 2:
        risk = "medium"
    else:
        risk = "low"

    audit = ReplyAudit(
        review_id=review_id,
        store_id=review.store_id,
        ai_reply_content=ai_reply,
        status="pending",
        risk_level=risk,
        scores=scores,
    )

    db.add(audit)
    await db.flush()
    return audit
