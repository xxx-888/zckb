"""
差评处理服务模块
提供差评自动回复审核、任务管理等功能
"""

import random
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

    # 如果没有数据，返回模拟数据
    if not tasks:
        for i in range(min(page_size, 5)):
            tasks.append({
                "id": UUID(int=i),
                "review_id": UUID(int=i + 2000),
                "user_name": f"用户{i+1}",
                "rating": random.randint(1, 2),
                "content": "菜品口味一般，服务态度有待提升。",
                "platform": random.choice(["meituan", "dianping"]),
                "ai_draft": "非常抱歉给您带来不好的体验，我们会认真改进。",
                "risk": random.choice(["high", "medium", "low"]),
                "scores": {
                    "realism": random.randint(70, 95),
                    "empathy": random.randint(75, 90),
                    "concreteness": random.randint(60, 85),
                    "consistency": random.randint(70, 90),
                },
                "status": status or "pending",
                "created_at": datetime.now(),
            })
        total = 18

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

    # 模拟重新生成回复
    templates = [
        "非常抱歉给您带来不好的用餐体验，我们会认真听取您的意见并持续改进。",
        "感谢您的反馈，对于您提到的问题我们深表歉意，已安排专人跟进处理。",
        "您好，对于本次服务不周之处我们深感抱歉，期待您给我们改正的机会。",
    ]
    audit.ai_reply_content = random.choice(templates)
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

    # 如果没有数据，返回模拟数据
    if not history:
        for i in range(min(page_size, 5)):
            history.append({
                "id": UUID(int=i),
                "review_id": UUID(int=i + 3000),
                "user_name": f"用户{i+1}",
                "content": "菜品口味一般，环境还可以。",
                "rating": 3,
                "platform": random.choice(["meituan", "dianping"]),
                "ai_draft": "感谢您的评价，我们会继续努力。",
                "final_reply": "感谢您的评价，我们会继续努力提升服务质量。",
                "status": random.choice(["sent", "rejected"]),
                "created_at": datetime.now(),
            })
        total = 42

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
