"""
经营洞察服务模块
提供菜品口碑分析、三好三差报告、服务案例库等功能
"""

import random
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review
from app.models.user import User


async def get_top_dishes(
    db: AsyncSession, user: User, period: str = "30d"
) -> list[dict]:
    """获取菜品口碑排行"""
    dishes = [
        {"name": "招牌红烧肉", "score": 4.8, "positive": 156, "negative": 8, "type": "recommend"},
        {"name": "清蒸鲈鱼", "score": 4.7, "positive": 142, "negative": 6, "type": "recommend"},
        {"name": "宫保鸡丁", "score": 4.5, "positive": 128, "negative": 12, "type": "recommend"},
        {"name": "麻婆豆腐", "score": 4.3, "positive": 115, "negative": 18, "type": "improve"},
        {"name": "糖醋排骨", "score": 4.2, "positive": 98, "negative": 22, "type": "improve"},
        {"name": "凉拌黄瓜", "score": 3.8, "positive": 45, "negative": 35, "type": "eliminate"},
        {"name": "酸辣汤", "score": 3.5, "positive": 38, "negative": 42, "type": "eliminate"},
    ]
    return dishes


async def get_three_good_three_bad(
    db: AsyncSession, user: User, period: str = "30d"
) -> dict:
    """获取三好三差报告"""
    return {
        "goods": [
            "服务态度热情周到，顾客满意度高",
            "招牌菜品口味稳定，复购率高",
            "用餐环境整洁舒适，氛围良好",
        ],
        "bads": [
            "高峰期上菜速度较慢，顾客等待时间长",
            "部分菜品分量不稳定，顾客反馈不一致",
            "停车便利性有待提升，影响顾客体验",
        ],
    }


async def get_dish_elimination(db: AsyncSession, user: User) -> list[dict]:
    """获取末位淘汰建议"""
    return [
        {
            "name": "凉拌黄瓜",
            "score": 3.8,
            "reason": "好评率低（56%），投诉较多，口味不稳定",
            "suggestion": "建议优化配方或从菜单中移除，替换为更受欢迎的凉菜",
        },
        {
            "name": "酸辣汤",
            "score": 3.5,
            "reason": "差评率高（52%），顾客反馈口味过酸或过辣",
            "suggestion": "建议调整配方比例，或更换为其他汤品",
        },
        {
            "name": "炒时蔬",
            "score": 3.9,
            "reason": "点单率低，利润率不高",
            "suggestion": "建议更换为季节性特色蔬菜，提升新鲜感和吸引力",
        },
    ]


async def get_service_cases(
    db: AsyncSession, user: User, case_type: str | None = None
) -> list[dict]:
    """获取服务案例库"""
    cases = [
        {
            "id": uuid4(),
            "type": "complaint",
            "content": "顾客投诉上菜时间过长，经核实为厨房高峰期出餐慢，已道歉并赠送甜品补偿。",
            "store_name": "总店",
            "created_at": datetime.now() - timedelta(days=2),
        },
        {
            "id": uuid4(),
            "type": "praise",
            "content": "顾客特别表扬服务员小李的贴心服务，主动为带小孩的顾客提供儿童座椅和餐具。",
            "store_name": "分店A",
            "created_at": datetime.now() - timedelta(days=5),
        },
        {
            "id": uuid4(),
            "type": "suggestion",
            "content": "顾客建议增加素食选项，已反馈给菜品研发部门。",
            "store_name": "分店B",
            "created_at": datetime.now() - timedelta(days=7),
        },
        {
            "id": uuid4(),
            "type": "complaint",
            "content": "顾客反映菜品中有异物，已退款并赠送优惠券，加强厨房卫生检查。",
            "store_name": "总店",
            "created_at": datetime.now() - timedelta(days=10),
        },
        {
            "id": uuid4(),
            "type": "praise",
            "content": "顾客表扬餐厅在生日时提供的惊喜服务，提升了用餐体验。",
            "store_name": "分店A",
            "created_at": datetime.now() - timedelta(days=12),
        },
    ]
    if case_type:
        cases = [c for c in cases if c["type"] == case_type]
    return cases


async def get_competitor_opportunities(db: AsyncSession, user: User) -> list[dict]:
    """获取同行机会洞察"""
    return [
        {
            "title": "下午茶市场空白",
            "description": "周边竞品较少提供下午茶服务，存在市场机会",
            "action_items": [
                "推出下午茶套餐，包含甜点和饮品",
                "在下午时段（14:00-17:00）推出优惠活动",
                "加强社交媒体宣传，吸引年轻客群",
            ],
        },
        {
            "title": "外卖渠道拓展",
            "description": "竞品外卖订单占比达35%，我方仅15%，增长空间大",
            "action_items": [
                "优化外卖包装设计，提升用户体验",
                "推出外卖专属套餐，提高性价比",
                "与更多外卖平台合作，扩大覆盖范围",
            ],
        },
        {
            "title": "会员体系升级",
            "description": "竞品会员复购率达60%，我方仅40%，需加强会员运营",
            "action_items": [
                "升级会员权益，增加专属优惠",
                "推出积分兑换系统，提升活跃度",
                "定期举办会员专属活动，增强粘性",
            ],
        },
    ]
