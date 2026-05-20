"""
审核服务模块
处理AI回复审核相关的业务逻辑
"""

import random
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.models.review import ReplyAudit, Review
from app.models.store import Store
from app.models.user import User


async def get_audit_list(
    db: AsyncSession,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[ReplyAudit], int]:
    """
    获取审核列表

    Args:
        db: 数据库会话
        status: 状态筛选（可选）
        keyword: 关键词搜索（可选）
        page: 页码
        page_size: 每页数量

    Returns:
        tuple: (审核列表, 总数)
    """
    conditions = []

    if status:
        conditions.append(ReplyAudit.status == status)

    where_clause = and_(*conditions) if conditions else True

    # 查询总数
    count_stmt = select(func.count()).select_from(ReplyAudit).where(where_clause)
    total = (await db.execute(count_stmt)).scalar() or 0

    # 分页查询
    offset = (page - 1) * page_size
    stmt = (
        select(ReplyAudit)
        .where(where_clause)
        .order_by(ReplyAudit.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    audits = list(result.scalars().all())

    return audits, total


async def get_audit_by_id(
    db: AsyncSession,
    audit_id: UUID,
) -> ReplyAudit:
    """
    根据ID获取审核记录

    Args:
        db: 数据库会话
        audit_id: 审核ID

    Returns:
        ReplyAudit: 审核记录对象

    Raises:
        NotFoundException: 审核记录不存在
    """
    result = await db.execute(
        select(ReplyAudit).where(ReplyAudit.id == audit_id)
    )
    audit = result.scalar_one_or_none()

    if not audit:
        raise NotFoundException("审核记录不存在")

    return audit


async def approve_audit(
    db: AsyncSession,
    audit_id: UUID,
    auditor_id: UUID,
) -> ReplyAudit:
    """
    审核通过

    Args:
        db: 数据库会话
        audit_id: 审核ID
        auditor_id: 审核人ID

    Returns:
        ReplyAudit: 更新后的审核记录

    Raises:
        NotFoundException: 审核记录不存在
        BusinessException: 审核状态不允许操作
    """
    audit = await get_audit_by_id(db, audit_id)

    if audit.status != "pending":
        raise BusinessException(f"审核状态为 '{audit.status}'，无法执行通过操作")

    audit.status = "approved"
    audit.auditor_id = auditor_id
    audit.reviewed_at = datetime.utcnow()

    # 更新评论的回复状态
    result = await db.execute(
        select(Review).where(Review.id == audit.review_id)
    )
    review = result.scalar_one_or_none()
    if review and audit.ai_reply_content:
        review.reply = audit.ai_reply_content
        review.reply_time = datetime.utcnow()
        review.ai_generated = True
        review.ai_reply_draft = None

    await db.flush()
    await db.refresh(audit)

    return audit


async def reject_audit(
    db: AsyncSession,
    audit_id: UUID,
    auditor_id: UUID,
    reason: str,
) -> ReplyAudit:
    """
    审核拒绝

    Args:
        db: 数据库会话
        audit_id: 审核ID
        auditor_id: 审核人ID
        reason: 拒绝原因

    Returns:
        ReplyAudit: 更新后的审核记录

    Raises:
        NotFoundException: 审核记录不存在
        BusinessException: 审核状态不允许操作
    """
    audit = await get_audit_by_id(db, audit_id)

    if audit.status != "pending":
        raise BusinessException(f"审核状态为 '{audit.status}'，无法执行拒绝操作")

    audit.status = "rejected"
    audit.auditor_id = auditor_id
    audit.reject_reason = reason
    audit.reviewed_at = datetime.utcnow()

    await db.flush()
    await db.refresh(audit)

    return audit


async def regenerate_reply(
    db: AsyncSession,
    audit_id: UUID,
) -> ReplyAudit:
    """
    重新生成AI回复

    Args:
        db: 数据库会话
        audit_id: 审核ID

    Returns:
        ReplyAudit: 更新后的审核记录

    Raises:
        NotFoundException: 审核记录不存在
        BusinessException: 审核状态不允许操作
    """
    audit = await get_audit_by_id(db, audit_id)

    if audit.status not in ("pending", "rejected"):
        raise BusinessException(f"审核状态为 '{audit.status}'，无法重新生成回复")

    # 获取评论内容
    result = await db.execute(
        select(Review).where(Review.id == audit.review_id)
    )
    review = result.scalar_one_or_none()

    if not review:
        raise NotFoundException("关联评论不存在")

    # 生成新的AI回复
    new_reply = await _generate_ai_reply(review.content, review.rating)

    audit.ai_reply_content = new_reply
    audit.status = "pending"
    audit.risk_level = _calculate_risk_level(review)
    audit.scores = _calculate_scores(new_reply)
    audit.reject_reason = None

    await db.flush()
    await db.refresh(audit)

    return audit


async def get_audit_stats(db: AsyncSession) -> dict:
    """
    获取审核统计数据

    Args:
        db: 数据库会话

    Returns:
        dict: 统计数据
    """
    # 各状态数量统计
    status_stmt = (
        select(ReplyAudit.status, func.count())
        .group_by(ReplyAudit.status)
    )
    status_result = await db.execute(status_stmt)
    status_map = dict(status_result.all())

    pending_count = status_map.get("pending", 0)
    approved_count = status_map.get("approved", 0)
    rejected_count = status_map.get("rejected", 0)
    total_count = sum(status_map.values())

    # 计算平均处理时间（已审核的记录）
    avg_time_stmt = select(
        func.avg(
            func.extract(
                "epoch",
                ReplyAudit.reviewed_at - ReplyAudit.created_at
            )
        )
    ).where(ReplyAudit.reviewed_at.isnot(None))
    avg_time = (await db.execute(avg_time_stmt)).scalar()

    avg_processing_time = round(float(avg_time), 2) if avg_time else None

    return {
        "pending_count": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "total_count": total_count,
        "avg_processing_time": avg_processing_time,
    }


async def _generate_ai_reply(review_content: Optional[str], rating: int) -> str:
    """
    生成AI回复（模拟实现）

    Args:
        review_content: 评论内容
        rating: 评分

    Returns:
        str: AI生成的回复
    """
    # 根据评分生成不同的回复模板
    if rating >= 4:
        templates = [
            "非常感谢您的认可和支持！我们会继续努力为您提供更好的服务和体验，期待您的再次光临！",
            "感谢您的五星好评！您的满意是我们最大的动力，我们会继续保持高标准的服务质量！",
            "非常感谢您的好评！我们会继续努力，为您带来更优质的体验！",
        ]
    elif rating == 3:
        templates = [
            "感谢您的反馈，我们会认真听取您的建议，不断改进和提升服务质量，期待为您提供更好的体验！",
            "谢谢您的评价，我们会继续努力改进，希望能为您提供更满意的服务！",
        ]
    else:
        templates = [
            "非常抱歉给您带来了不好的体验，我们会认真反思并改进。如果您愿意，欢迎联系我们，我们会尽力为您解决问题。",
            "对于您的不满意，我们深表歉意。您的反馈对我们很重要，我们会立即改进相关问题。",
            "非常抱歉没有让您满意，我们会认真对待您的反馈，努力提升服务质量。",
        ]

    return random.choice(templates)


def _calculate_risk_level(review: Review) -> str:
    """
    计算风险等级

    Args:
        review: 评论对象

    Returns:
        str: 风险等级 (high/medium/low)
    """
    # 基于评分和情感计算风险等级
    if review.rating <= 2:
        return "high"
    elif review.rating == 3:
        return "medium"
    else:
        return "low"


def _calculate_scores(ai_reply: str) -> dict:
    """
    计算AI回复的各项评分

    Args:
        ai_reply: AI回复内容

    Returns:
        dict: 各项评分
    """
    # 模拟评分计算
    return {
        "realism": round(random.uniform(0.7, 0.95), 2),      # 真实性
        "empathy": round(random.uniform(0.6, 0.9), 2),       # 共情度
        "concreteness": round(random.uniform(0.5, 0.85), 2), # 具体性
        "consistency": round(random.uniform(0.7, 0.95), 2),  # 一致性
    }
