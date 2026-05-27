"""
用户区域关联服务层
处理用户与区域的关联关系，以及区域权限相关的业务逻辑
"""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.region import Region
from app.models.user import User
from app.models.user_region import user_regions


async def get_user_regions(db: AsyncSession, user_id: UUID) -> list[dict]:
    """
    获取用户关联的区域列表（包括子级区域统计）
    
    Args:
        db: 异步数据库会话
        user_id: 用户ID
        
    Returns:
        list[dict]: 区域列表，每个区域包含基本信息
    """
    # 查询用户关联的区域
    result = await db.execute(
        select(Region)
        .join(user_regions)
        .where(user_regions.c.user_id == user_id)
    )
    regions = result.scalars().all()
    
    # 构建返回数据
    regions_data = []
    for region in regions:
        # 统计该区域下的店铺数量
        store_count = len(region.stores) if region.stores else 0
        
        regions_data.append({
            "id": str(region.id),
            "name": region.name,
            "level": region.level,
            "code": region.code,
            "store_count": store_count,
        })
    
    return regions_data


async def add_user_region(db: AsyncSession, user_id: UUID, region_id: UUID) -> dict:
    """
    添加用户区域关联
    
    Args:
        db: 异步数据库会话
        user_id: 用户ID
        region_id: 区域ID
        
    Returns:
        dict: 操作结果
    """
    from sqlalchemy import insert
    from sqlalchemy.exc import IntegrityError
    
    # 检查用户是否存在
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise ValueError("用户不存在")
    
    # 检查区域是否存在
    region_result = await db.execute(select(Region).where(Region.id == region_id))
    region = region_result.scalar_one_or_none()
    if not region:
        raise ValueError("区域不存在")
    
    # 添加关联（处理唯一约束冲突）
    try:
        await db.execute(insert(user_regions).values(user_id=user_id, region_id=region_id))
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("用户已关联该区域")
    
    return {"message": "添加成功"}


async def remove_user_region(db: AsyncSession, user_id: UUID, region_id: UUID) -> dict:
    """
    移除用户区域关联
    
    Args:
        db: 异步数据库会话
        user_id: 用户ID
        region_id: 区域ID
        
    Returns:
        dict: 操作结果
    """
    from sqlalchemy import delete
    
    # 检查用户是否存在
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise ValueError("用户不存在")
    
    # 检查区域是否存在
    region_result = await db.execute(select(Region).where(Region.id == region_id))
    region = region_result.scalar_one_or_none()
    if not region:
        raise ValueError("区域不存在")
    
    # 删除关联
    result = await db.execute(
        delete(user_regions).where(
            user_regions.c.user_id == user_id,
            user_regions.c.region_id == region_id
        )
    )
    
    if result.rowcount == 0:
        raise ValueError("用户未关联该区域")
    
    await db.commit()
    
    return {"message": "移除成功"}


async def get_all_sub_region_ids(db: AsyncSession, region_id: UUID) -> List[UUID]:
    """
    递归获取某个区域的所有子级区域ID（包括自己）
    用于动态查询，不存储冗余数据
    
    Args:
        db: 异步数据库会话
        region_id: 区域ID
        
    Returns:
        List[UUID]: 包含所有子级区域ID的列表（包括自己）
    """
    result = [region_id]
    
    # 查询直接子级
    sub_result = await db.execute(
        select(Region.id).where(Region.parent_id == region_id)
    )
    sub_regions = sub_result.all()
    
    # 递归查询每个子级的子级
    for (sub_id,) in sub_regions:
        sub_ids = await get_all_sub_region_ids(db, sub_id)
        result.extend(sub_ids)
    
    return result


async def get_user_accessible_region_ids(db: AsyncSession, user_id: UUID) -> List[UUID]:
    """
    获取用户可访问的所有区域ID（包括子级）
    用于权限过滤
    
    Args:
        db: 异步数据库会话
        user_id: 用户ID
        
    Returns:
        List[UUID]: 可访问的区域ID列表（去重），空列表表示无限制
    """
    # 查询用户
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        return []
    
    # 超级管理员不受限制，返回空列表表示无限制
    if user.role in ["SUPER_ADMIN", "HQ"]:
        return []  # 空列表表示无限制
    
    # 获取用户关联的区域
    region_result = await db.execute(
        select(Region).join(user_regions).where(user_regions.c.user_id == user_id)
    )
    regions = region_result.scalars().all()
    
    # 动态查询所有子级区域
    region_ids = []
    for region in regions:
        sub_ids = await get_all_sub_region_ids(db, region.id)
        region_ids.extend(sub_ids)
    
    # 去重
    return list(set(region_ids))


async def get_regions_with_children(db: AsyncSession, parent_id: Optional[UUID] = None) -> list[dict]:
    """
    获取区域树形结构（用于前端树形选择器）
    
    Args:
        db: 异步数据库会话
        parent_id: 父级区域ID，None 表示查询所有顶级区域（province）
        
    Returns:
        list[dict]: 树形结构
    """
    # 构建查询条件
    if parent_id:
        result = await db.execute(
            select(Region).where(Region.parent_id == parent_id).order_by(Region.code.asc())
        )
    else:
        result = await db.execute(
            select(Region).where(Region.parent_id.is_(None)).order_by(Region.code.asc())
        )
    
    regions = result.scalars().all()
    
    # 构建树形结构
    result_list = []
    for region in regions:
        # 递归获取子级
        children = await get_regions_with_children(db, region.id)
        
        result_list.append({
            "id": str(region.id),
            "name": region.name,
            "level": region.level,
            "code": region.code,
            "children": children if children else [],
        })
    
    return result_list
