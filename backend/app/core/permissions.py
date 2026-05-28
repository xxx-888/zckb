"""
权限管理装饰器
提供超级管理员权限检查、数据范围过滤等功能
"""

from functools import wraps
from typing import Callable, List, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.core.database import get_db
from app.models.user import User, UserStore
from app.models.store import Store


async def get_data_scope(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    获取数据范围依赖
    超级管理员：返回 None（不过滤）
    非超级管理员：返回店铺ID列表
    
    Usage:
        @router.get("/reviews")
        async def get_reviews(
            store_ids: Optional[List] = Depends(get_data_scope),
            db: AsyncSession = Depends(get_db),
        ):
            if store_ids is not None:
                # 过滤店铺
                query = query.where(Review.store_id.in_(store_ids))
    """
    # 超级管理员可以查看所有数据
    if user.role == "SUPER_ADMIN":
        return None
    
    # 非超级管理员只能查看关联的店铺
    # 查询用户关联的店铺
    result = await db.execute(
        select(UserStore.store_id).where(UserStore.user_id == user.id)
    )
    associated_store_ids = [row[0] for row in result.all()]
    
    # 查询用户拥有的店铺
    result = await db.execute(
        select(Store.id).where(Store.owner_id == user.id)
    )
    owned_store_ids = [row[0] for row in result.all()]
    
    # 合并店铺ID
    store_ids = list(set(associated_store_ids + owned_store_ids))
    
    return store_ids if store_ids else []


# 兼容旧名称
get_data_scope_filter = get_data_scope


def super_admin_required(
    current_user: User = Depends(get_current_user),
):
    """
    超级管理员权限检查依赖
    只有 SUPER_ADMIN 角色的用户才能访问
    
    Usage:
        @router.get("/admin-only")
        async def admin_route(
            user: User = Depends(super_admin_required),
        ):
            ...
    """
    if current_user.role != "SUPER_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要超级管理员权限"
        )
    return current_user


def apply_store_filter(query, model, store_ids: Optional[List]):
    """
    应用店铺过滤条件到查询
    
    Args:
        query: SQLAlchemy查询对象
        model: 模型类
        store_ids: 店铺ID列表（None表示不过滤）
        
    Returns:
        过滤后的查询对象
    """
    if store_ids is None:
        # 超级管理员，不过滤
        return query
    
    if not store_ids:
        # 没有关联店铺，返回空结果
        return query.where(False)
    
    # 添加店铺ID过滤条件
    return query.where(model.store_id.in_(store_ids))
