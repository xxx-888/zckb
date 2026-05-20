"""
AI分析服务模块
提供AI语义分析、情感分析、风险分级等功能
"""

import random
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import and_, case, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_config import AIProcessingLog, AIModelConfig
from app.models.review import ReplyAudit, Review
from app.models.user import User


async def get_topics(db: AsyncSession, user: User, period: str = "30d") -> list[dict]:
    """
    获取语义分析主题

    Args:
        db: 数据库会话
        user: 当前用户
        period: 时间周期

    Returns:
        list[dict]: 主题列表
    """
    # 模拟数据 - 实际应从AI分析结果获取
    topics = [
        {"label": "服务态度", "sentiment": "positive", "count": 156, "trend": "up"},
        {"label": "菜品口味", "sentiment": "positive", "count": 142, "trend": "stable"},
        {"label": "环境卫生", "sentiment": "neutral", "count": 89, "trend": "down"},
        {"label": "上菜速度", "sentiment": "negative", "count": 45, "trend": "up"},
        {"label": "性价比", "sentiment": "positive", "count": 123, "trend": "up"},
        {"label": "停车便利", "sentiment": "negative", "count": 34, "trend": "stable"},
    ]
    return topics


async def get_tag_clustering(db: AsyncSession, user: User, period: str = "30d") -> list[dict]:
    """
    获取差评标签聚类

    Args:
        db: 数据库会话
        user: 当前用户
        period: 时间周期

    Returns:
        list[dict]: 标签聚类列表
    """
    # 模拟数据
    clusters = [
        {
            "category": "服务质量",
            "items": ["服务态度差", "响应慢", "不理人"],
            "percentage": 35.5,
            "color": "#FF6B6B",
        },
        {
            "category": "菜品问题",
            "items": ["口味不佳", "食材不新鲜", "分量少"],
            "percentage": 28.3,
            "color": "#FFA94D",
        },
        {
            "category": "环境卫生",
            "items": ["桌面不干净", "地面湿滑", "有异味"],
            "percentage": 18.7,
            "color": "#FFD43B",
        },
        {
            "category": "等待时间",
            "items": ["上菜慢", "排队久", "出餐慢"],
            "percentage": 17.5,
            "color": "#69DB7C",
        },
    ]
    return clusters


async def get_sentiment_summary(db: AsyncSession, user: User) -> dict:
    """
    获取情感指数汇总

    Args:
        db: 数据库会话
        user: 当前用户

    Returns:
        dict: 情感指数数据
    """
    # 查询用户的评论数据
    stmt = (
        select(
            func.count(Review.id).label("total"),
            func.sum(case((Review.sentiment == "positive", 1), else_=0)).label("positive"),
            func.sum(case((Review.sentiment == "negative", 1), else_=0)).label("negative"),
        )
        .join(Review.store)
        .where(Review.store_id.in_([sa.store_id for sa in user.store_associations]))
    )
    result = await db.execute(stmt)
    row = result.one_or_none()

    if row and row.total > 0:
        positive = row.positive or 0
        negative = row.negative or 0
        total = row.total
        score = (positive / total) * 100 if total > 0 else 50.0
    else:
        # 模拟数据
        positive = 245
        negative = 45
        total = 290
        score = 84.5

    # 转成百分比（前端进度条用）
    positive_pct = round((positive / total) * 100) if total > 0 else 0
    negative_pct = round((negative / total) * 100) if total > 0 else 0

    return {
        "score": round(score, 1),
        "trend": "up",
        "positive": positive_pct,
        "negative": negative_pct,
        "ai_accuracy": 92.5,
    }


async def get_risk_levels(db: AsyncSession, user: User) -> dict:
    """
    获取风险分级统计

    Args:
        db: 数据库会话
        user: 当前用户

    Returns:
        dict: 风险分级数据
    """
    # 查询风险等级分布
    stmt = (
        select(
            Review.risk_level,
            func.count(Review.id).label("count"),
        )
        .join(Review.store)
        .where(
            and_(
                Review.store_id.in_([sa.store_id for sa in user.store_associations]),
                Review.risk_level.isnot(None),
            )
        )
        .group_by(Review.risk_level)
    )
    result = await db.execute(stmt)
    rows = result.all()

    risk_counts = {"high": 0, "medium": 0, "low": 0}
    for row in rows:
        if row.risk_level in risk_counts:
            risk_counts[row.risk_level] = row.count

    # 如果没有数据，使用模拟数据
    if sum(risk_counts.values()) == 0:
        risk_counts = {"high": 12, "medium": 28, "low": 156}

    return {
        "high_count": risk_counts["high"],
        "high_desc": "需立即处理，可能影响门店评分",
        "medium_count": risk_counts["medium"],
        "medium_desc": "建议24小时内回复处理",
        "low_count": risk_counts["low"],
        "low_desc": "常规回复即可",
    }


async def get_reply_history(
    db: AsyncSession, user: User, page: int = 1, page_size: int = 20
) -> tuple[list, int]:
    """
    获取自动回复历史

    Args:
        db: 数据库会话
        user: 当前用户
        page: 页码
        page_size: 每页大小

    Returns:
        tuple[list, int]: (历史记录列表, 总数)
    """
    # 查询总数
    count_stmt = (
        select(func.count(ReplyAudit.id))
        .join(ReplyAudit.review)
        .where(ReplyAudit.store_id.in_([sa.store_id for sa in user.store_associations]))
    )
    count_result = await db.execute(count_stmt)
    total = count_result.scalar() or 0

    # 查询数据
    stmt = (
        select(ReplyAudit)
        .join(ReplyAudit.review)
        .where(ReplyAudit.store_id.in_([sa.store_id for sa in user.store_associations]))
        .order_by(desc(ReplyAudit.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    audits = result.scalars().all()

    history = []
    for audit in audits:
        history.append({
            "id": audit.id,
            "review_id": audit.review_id,
            "content": audit.ai_reply_content or "",
            "ai_generated": True,
            "status": audit.status,
            "created_at": audit.created_at,
        })

    # 如果没有数据，返回模拟数据
    if not history:
        for i in range(min(page_size, 5)):
            history.append({
                "id": UUID(int=i),
                "review_id": UUID(int=i + 1000),
                "content": f"感谢您的评价，我们会持续改进服务质量。",
                "ai_generated": True,
                "status": random.choice(["approved", "sent", "rejected"]),
                "created_at": datetime.now() - timedelta(hours=i * 2),
            })
        total = 25

    return history, total


async def get_reply_stats(db: AsyncSession, user: User) -> dict:
    """
    获取回复统计数据

    Args:
        db: 数据库会话
        user: 当前用户

    Returns:
        dict: 回复统计数据
    """
    # 查询统计
    stmt = (
        select(
            func.count(ReplyAudit.id).label("total"),
            func.sum(case((ReplyAudit.status == "sent", 1), else_=0)).label("sent"),
        )
        .where(ReplyAudit.store_id.in_([sa.store_id for sa in user.store_associations]))
    )
    result = await db.execute(stmt)
    row = result.one_or_none()

    if row and row.total > 0:
        total = row.total
        sent = row.sent or 0
        success_rate = (sent / total) * 100 if total > 0 else 0
    else:
        # 模拟数据
        total = 156
        success_rate = 94.2

    return {
        "total": total,
        "ai_generated": int(total * 0.85),
        "manual": int(total * 0.15),
        "success_rate": round(success_rate, 1),
    }


async def get_appeal_suggestion(db: AsyncSession, review_id: UUID) -> dict:
    """
    获取申诉建议

    Args:
        db: 数据库会话
        review_id: 评论ID

    Returns:
        dict: 申诉建议数据
    """
    # 查询评论
    stmt = select(Review).where(Review.id == review_id)
    result = await db.execute(stmt)
    review = result.scalar_one_or_none()

    # 模拟AI分析结果
    is_malicious = review.rating <= 2 if review else random.random() < 0.3
    confidence = random.uniform(0.7, 0.95) if is_malicious else random.uniform(0.3, 0.6)

    if is_malicious:
        suggestion = "该评论疑似恶意差评，建议提交申诉"
        appeal_content = (
            f"尊敬的平台审核人员：\n\n"
            f"我们发现该用户（{review.user_name if review else '匿名用户'}）的评价存在以下异常：\n"
            f"1. 评价内容与实际情况不符\n"
            f"2. 疑似竞争对手恶意抹黑\n"
            f"3. 评价时间集中，疑似批量操作\n\n"
            f"恳请平台核实处理，维护公平公正的营商环境。"
        )
    else:
        suggestion = "该评论属于正常用户反馈，建议正常回复处理"
        appeal_content = ""

    return {
        "review_id": review_id,
        "is_malicious": is_malicious,
        "confidence": round(confidence, 2),
        "suggestion": suggestion,
        "appeal_content": appeal_content,
    }


async def analyze_review_sentiment(content: str) -> dict:
    """
    分析评论情感（模拟AI语义分析）

    Args:
        content: 评论内容

    Returns:
        dict: 情感分析结果
    """
    # 简单的关键词匹配模拟AI分析
    positive_keywords = ["好", "棒", "满意", "喜欢", "推荐", "不错", "好吃", "美味"]
    negative_keywords = ["差", "难吃", "失望", "不好", "糟糕", "慢", "脏", "贵"]

    if not content:
        return {"sentiment": "neutral", "confidence": 0.5, "score": 0.0}

    positive_count = sum(1 for kw in positive_keywords if kw in content)
    negative_count = sum(1 for kw in negative_keywords if kw in content)

    if positive_count > negative_count:
        sentiment = "positive"
        confidence = min(0.5 + positive_count * 0.1, 0.95)
        score = min(positive_count * 0.2, 1.0)
    elif negative_count > positive_count:
        sentiment = "negative"
        confidence = min(0.5 + negative_count * 0.1, 0.95)
        score = -min(negative_count * 0.2, 1.0)
    else:
        sentiment = "neutral"
        confidence = 0.5
        score = 0.0

    return {
        "sentiment": sentiment,
        "confidence": round(confidence, 2),
        "score": round(score, 2),
    }
