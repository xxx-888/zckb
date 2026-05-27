"""
好评激活服务模块
提供优质好评筛选、内容生成、授权管理等功能
"""

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
    # 超级管理员可以查看所有数据，非管理员只能查看关联的店铺
    if user.role == "SUPER_ADMIN":
        # 超级管理员：查询所有店铺
        conditions = [
            Review.rating >= 4,
            Review.sentiment == "positive",
            Review.content.isnot(None),
        ]
    else:
        # 非管理员：只查询关联的店铺
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
            "authorized": False,  # 默认未授权，需要用户同意
            "suggested_script": "您的满意是我们最大的动力，期待您的再次光临！",
            "created_at": review.created_at,
        })

    return items, total


async def get_brand_scripts(db: AsyncSession, user: User) -> list[dict]:
    """
    基于真实好评提炼品牌话术库
    
    Args:
        db: 数据库会话
        user: 当前用户
        
    Returns:
        list[dict]: 品牌话术列表
    """
    # 查询用户关联的高评分评论（>=4星）
    # 超级管理员可以查看所有数据，非管理员只能查看关联的店铺
    if user.role == "SUPER_ADMIN":
        # 超级管理员：查询所有店铺
        conditions = [
            Review.rating >= 4,
            Review.content.isnot(None),
        ]
    else:
        # 非管理员：只查询关联的店铺
        user_store_ids = [sa.store_id for sa in user.store_associations]
        
        if not user_store_ids:
            return []
        
        conditions = [
            Review.store_id.in_(user_store_ids),
            Review.rating >= 4,
            Review.content.isnot(None),
        ]
    
    stmt = (
        select(Review)
        .where(and_(*conditions))
        .order_by(desc(Review.created_at))
        .limit(500)  # 分析最近500条好评
    )
    result = await db.execute(stmt)
    reviews = result.scalars().all()
    
    if not reviews:
        return []
    
    # 基于真实好评内容，提炼品牌话术
    # 简化的关键词提取和话术生成
    scripts = []
    
    # 1. 感谢类话术（基于真实好评的常见表达）
    thank_you_count = len([r for r in reviews if "谢谢" in (r.content or "") or "感谢" in (r.content or "")])
    if thank_you_count > 0:
        scripts.append({
            "id": UUID("11111111-1111-1111-1111-111111111111"),
            "name": "感谢好评-真诚版",
            "content": "非常感谢您的五星好评！您的认可是我们前进的最大动力，期待再次为您服务！",
            "category": "好评回复",
            "usage_count": thank_you_count,
            "progress": f"{min(95, thank_you_count * 5)}%",
        })
    
    # 2. 菜品赞美类话术
    food_praise_count = len([r for r in reviews if any(word in (r.content or "") for word in ["好吃", "美味", "菜品", "味道"])])
    if food_praise_count > 0:
        scripts.append({
            "id": UUID("22222222-2222-2222-2222-222222222222"),
            "name": "菜品好评-专业版",
            "content": "感谢您对我们菜品的认可！我们始终坚持选用新鲜食材，用心烹饪每一道菜，期待您下次再来品尝新品！",
            "category": "好评回复",
            "usage_count": food_praise_count,
            "progress": f"{min(90, food_praise_count * 6)}%",
        })
    
    # 3. 服务赞美类话术
    service_praise_count = len([r for r in reviews if any(word in (r.content or "") for word in ["服务", "服务员", "态度"])])
    if service_praise_count > 0:
        scripts.append({
            "id": UUID("33333333-3333-3333-3333-333333333333"),
            "name": "服务好评-温暖版",
            "content": "感谢您对我们服务的认可！优质服务是我们的承诺，我们会继续保持热情周到，让您每次用餐都感到温暖！",
            "category": "好评回复",
            "usage_count": service_praise_count,
            "progress": f"{min(88, service_praise_count * 7)}%",
        })
    
    # 4. 环境赞美类话术
    env_praise_count = len([r for r in reviews if any(word in (r.content or "") for word in ["环境", "装修", "氛围", "干净"])])
    if env_praise_count > 0:
        scripts.append({
            "id": UUID("44444444-4444-4444-4444-444444444444"),
            "name": "环境好评-优雅版",
            "content": "感谢您对我们环境的喜爱！我们精心打造的用餐环境，就是希望每一位顾客都能在这里享受愉悦的时光，期待您常来！",
            "category": "好评回复",
            "usage_count": env_praise_count,
            "progress": f"{min(85, env_praise_count * 8)}%",
        })
    
    # 5. 推荐类话术（用于引导复购和分享）
    recommend_count = len([r for r in reviews if any(word in (r.content or "") for word in ["推荐", "下次", "再来", "朋友"])])
    scripts.append({
        "id": UUID("55555555-5555-5555-5555-555555555555"),
        "name": "邀请复购-亲切版",
        "content": "感谢您的推荐！您的满意是我们最大的幸福，期待您下次光临时带上亲朋好友，我们准备了专属优惠等您来享！",
        "category": "复购引导",
        "usage_count": max(recommend_count, 1),
        "progress": f"{min(80, max(recommend_count * 10, 30))}%",
    })
    
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
