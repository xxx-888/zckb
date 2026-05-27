"""
好评激活服务模块
提供优质好评筛选、内容生成、授权管理等功能
"""

import random
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.review import Review
from app.models.user import User, UserStore
from app.models.store import Store
async def get_high_quality_reviews(
    db: AsyncSession, user: User, page: int = 1, page_size: int = 20
) -> tuple[list, int]:
    """
    获取优质好评列表

    Args:
        db: 数据库会话
        user: 当前用户
        page: 页码
        page_size: 每页大小

    Returns:
        tuple[list, int]: (好评列表, 总数)
    """
    # 构建查询条件：高评分、有内容、正面情感
    # 获取用户关联的店铺ID
    # 查询用户拥有的店铺
    owned_stores_result = await db.execute(
        select(Store.id).where(Store.owner_id == user.id)
    )
    owned_store_ids = [row[0] for row in owned_stores_result.all()]
    
    # 查询用户关联的店铺（通过 user_stores 表）
    associated_stores_result = await db.execute(
        select(UserStore.store_id).where(UserStore.user_id == user.id)
    )
    associated_store_ids = [row[0] for row in associated_stores_result.all()]
    
    # 合并店铺ID
    user_store_ids = list(set(owned_store_ids + associated_store_ids))
    
    if not user_store_ids:
        return [], 0
    
    conditions = [
        Review.store_id.in_(user_store_ids),
        Review.rating >= 4,
        Review.sentiment == "positive",
        Review.content.isnot(None),
    ]

    # 查询总数
    count_stmt = select(func.count(Review.id)).where(and_(*conditions))
    count_result = await db.execute(count_stmt)
    total = count_result.scalar() or 0

    # 查询数据
    stmt = (
        select(Review)
        .where(and_(*conditions))
        .order_by(desc(Review.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    reviews = result.scalars().all()

    items = []
    for review in reviews:
        items.append({
            "id": review.id,
            "user_name": review.user_name,
            "avatar": review.user_avatar,
            "content": review.content,
            "rating": review.rating,
            "has_image": bool(review.images and len(review.images) > 0),
            "length": len(review.content) if review.content else 0,
            "sentiment": review.sentiment or "positive",
            "authorized": random.choice([True, False]),  # 模拟授权状态
            "suggested_script": "您的满意是我们最大的动力，期待您的再次光临！",
            "created_at": review.created_at,
        })

    # 如果没有数据，返回模拟数据
    if not items:
        for i in range(min(page_size, 5)):
            items.append({
                "id": UUID(int=i),
                "user_name": f"美食家{i+1}",
                "avatar": None,
                "content": "这家餐厅真的太棒了！菜品精致美味，服务热情周到，环境优雅舒适，强烈推荐给大家！",
                "rating": 5,
                "has_image": random.choice([True, False]),
                "length": 45,
                "sentiment": "positive",
                "authorized": random.choice([True, False]),
                "suggested_script": "感谢您的五星好评，期待再次为您服务！",
                "created_at": datetime.now() - timedelta(days=i),
            })
        total = 28

    return items, total


async def get_brand_scripts(db: AsyncSession) -> list[dict]:
    """
    获取品牌话术库

    Args:
        db: 数据库会话

    Returns:
        list[dict]: 品牌话术列表
    """
    # 模拟品牌话术数据
    scripts = [
        {
            "id": UUID(int=1),
            "name": "感谢好评-通用版",
            "content": "感谢您的五星好评，您的满意是我们全体团队前进的动力！",
            "category": "好评回复",
            "usage_count": 1256,
            "progress": "92%",  # 添加progress字段
        },
        {
            "id": UUID(int=2),
            "name": "感谢好评-详细版",
            "content": "非常感谢您的详细评价和认可！我们会继续保持品质，期待您的再次光临！",
            "category": "好评回复",
            "usage_count": 892,
            "progress": "78%",
        },
        {
            "id": UUID(int=3),
            "name": "邀请复购话术",
            "content": "感谢您的认可！下次光临时出示此评价可享专属优惠哦~",
            "category": "复购引导",
            "usage_count": 567,
            "progress": "65%",
        },
        {
            "id": UUID(int=4),
            "name": "小红书种草模板",
            "content": "发现一家宝藏餐厅！环境超赞，菜品精致，拍照打卡圣地~",
            "category": "种草文案",
            "usage_count": 423,
            "progress": "58%",
        },
        {
            "id": UUID(int=5),
            "name": "抖音推广话术",
            "content": "这家店真的绝了！每一道菜都是惊喜，强烈推荐给大家！",
            "category": "种草文案",
            "usage_count": 389,
            "progress": "45%",
        },
    ]
    return scripts


async def copy_script(db: AsyncSession, script_id: UUID) -> None:
    """
    记录话术复制

    Args:
        db: 数据库会话
        script_id: 话术ID

    Returns:
        None
    """
    # 实际应用中应记录用户复制行为
    # 这里仅作模拟
    pass


async def send_authorization(db: AsyncSession, review_id: UUID) -> None:
    """
    发送授权请求

    Args:
        db: 数据库会话
        review_id: 评论ID

    Returns:
        None
    """
    stmt = select(Review).where(Review.id == review_id)
    result = await db.execute(stmt)
    review = result.scalar_one_or_none()

    if not review:
        raise NotFoundException("评论不存在")

    # 实际应用中应发送授权请求通知
    # 这里仅作模拟
    pass


async def generate_content(db: AsyncSession, review_id: UUID, platform: str) -> dict:
    """
    生成种草内容

    Args:
        db: 数据库会话
        review_id: 评论ID
        platform: 目标平台

    Returns:
        dict: 生成的内容
    """
    stmt = select(Review).where(Review.id == review_id)
    result = await db.execute(stmt)
    review = result.scalar_one_or_none()

    if not review:
        raise NotFoundException("评论不存在")

    # 根据平台生成不同风格的内容
    platform_templates = {
        "xiaohongshu": {
            "content": (
                f"发现一家超棒的餐厅！🍽️\n\n"
                f"{review.content if review.content else '菜品精致，环境优雅，服务贴心'}\n\n"
                f"拍照超出片，氛围感满满~\n"
                f"姐妹们快冲！💕"
            ),
            "hashtags": ["#美食探店", "#宝藏餐厅", "#美食打卡", "#生活美学"],
        },
        "douyin": {
            "content": (
                f"这家店真的绝了！🔥\n\n"
                f"{review.content if review.content else '每一道菜都是惊喜'}\n\n"
                f"好吃到停不下来，强烈推荐！"
            ),
            "hashtags": ["#美食推荐", "#探店", "#吃货日常", "#美食vlog"],
        },
        "weibo": {
            "content": (
                f"今日美食分享 ✨\n\n"
                f"{review.content if review.content else '发现一家不错的餐厅'}\n\n"
                f"值得一试~"
            ),
            "hashtags": ["#美食", "#餐厅推荐", "#生活碎片"],
        },
    }

    template = platform_templates.get(platform, platform_templates["xiaohongshu"])

    return {
        "review_id": review_id,
        "content": template["content"],
        "platform": platform,
        "hashtags": template["hashtags"],
    }
