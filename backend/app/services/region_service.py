"""Region Service - 区域管理业务逻辑"""

from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.region import Region
from app.schemas.region import RegionCreate, RegionUpdate


# ========================
# 内部工具函数
# ========================

def _region_to_dict(region: Region) -> Dict[str, Any]:
    """将 Region ORM 对象转换为字典（处理 UUID 和关系）"""
    parent_dict = None
    if region.parent:
        parent_dict = {
            "id": str(region.parent.id),
            "name": region.parent.name,
            "level": region.parent.level,
            "code": region.parent.code,
        }
    
    children_dicts = []
    for child in region.children:
        children_dicts.append({
            "id": str(child.id),
            "name": child.name,
            "level": child.level,
            "code": child.code,
        })
    
    return {
        "id": str(region.id),
        "name": region.name,
        "parent_id": str(region.parent_id) if region.parent_id else None,
        "level": region.level,
        "code": region.code,
        "created_at": region.created_at,
        "updated_at": region.updated_at,
        "parent": parent_dict,
        "children": children_dicts,
        "store_count": len(region.stores) if region.stores else 0,
    }


# ========================
# 查询函数
# ========================

async def get_regions(
    db: AsyncSession,
    parent_id: Optional[str] = None,
    level: Optional[str] = None,
    tree: bool = False,
) -> List[Dict[str, Any]]:
    """
    获取区域列表（返回字典列表，避免 ORM 序列化问题）
    """
    stmt = select(Region).options(
        selectinload(Region.parent),
        selectinload(Region.children),
        selectinload(Region.stores),
    )
    
    if parent_id is not None:
        stmt = stmt.where(Region.parent_id == UUID(parent_id))
    elif not tree:
        pass  # 返回所有
    
    if level:
        stmt = stmt.where(Region.level == level)
    
    stmt = stmt.order_by(Region.name)
    
    result = await db.execute(stmt)
    regions = result.scalars().all()
    
    if tree:
        regions = [r for r in regions if r.parent_id is None]
    
    return [_region_to_dict(r) for r in regions]


async def get_region(db: AsyncSession, region_id: str) -> Optional[Dict[str, Any]]:
    """根据ID获取单个区域"""
    stmt = select(Region).options(
        selectinload(Region.parent),
        selectinload(Region.children),
        selectinload(Region.stores),
    ).where(Region.id == UUID(region_id))
    
    result = await db.execute(stmt)
    region = result.scalar_one_or_none()
    
    if region is None:
        return None
    return _region_to_dict(region)


async def get_region_tree(db: AsyncSession) -> List[Dict[str, Any]]:
    """获取区域树形结构"""
    stmt = select(Region).options(
        selectinload(Region.children),
        selectinload(Region.stores),
    ).order_by(Region.name)
    
    result = await db.execute(stmt)
    all_regions = result.scalars().all()
    
    # 构建 ID 到字典的映射
    region_dicts = {}
    for region in all_regions:
        region_dicts[str(region.id)] = {
            "id": str(region.id),
            "name": region.name,
            "level": region.level,
            "code": region.code,
            "children": [],
        }
    
    # 构建树形结构
    tree = []
    for region in all_regions:
        region_dict = region_dicts[str(region.id)]
        if region.parent_id:
            parent_id = str(region.parent_id)
            if parent_id in region_dicts:
                region_dicts[parent_id]["children"].append(region_dict)
        else:
            tree.append(region_dict)
    
    return tree


# ========================
# 写入函数
# ========================

async def create_region(db: AsyncSession, data: RegionCreate) -> Dict[str, Any]:
    """创建新区域"""
    region_data = data.model_dump()
    
    if "parent_id" in region_data:
        if region_data["parent_id"] == "":
            region_data["parent_id"] = None
        elif region_data["parent_id"]:
            region_data["parent_id"] = UUID(region_data["parent_id"])
    
    region = Region(**region_data)
    db.add(region)
    await db.flush()
    await db.refresh(region, attribute_names=["stores"])
    
    # 重新加载关系
    stmt = select(Region).options(
        selectinload(Region.parent),
        selectinload(Region.children),
        selectinload(Region.stores),
    ).where(Region.id == region.id)
    
    result = await db.execute(stmt)
    region = result.scalar_one()
    
    return _region_to_dict(region)


async def update_region(
    db: AsyncSession, region_id: str, data: RegionUpdate
) -> Optional[Dict[str, Any]]:
    """更新区域"""
    stmt = select(Region).options(
        selectinload(Region.parent),
        selectinload(Region.children),
        selectinload(Region.stores),
    ).where(Region.id == UUID(region_id))
    
    result = await db.execute(stmt)
    region = result.scalar_one_or_none()
    
    if region is None:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    
    if "parent_id" in update_data:
        if update_data["parent_id"] == "":
            update_data["parent_id"] = None
        elif update_data["parent_id"]:
            update_data["parent_id"] = UUID(update_data["parent_id"])
    
    for field, value in update_data.items():
        setattr(region, field, value)
    
    await db.flush()
    return _region_to_dict(region)


async def delete_region(db: AsyncSession, region_id: str) -> bool:
    """删除区域（有关联门店或子级区域则禁止删除）"""
    stmt = select(Region).options(
        selectinload(Region.children),
        selectinload(Region.stores),
    ).where(Region.id == UUID(region_id))
    
    result = await db.execute(stmt)
    region = result.scalar_one_or_none()
    
    if region is None:
        return False
    
    # 检查是否有关联门店
    if region.stores and len(region.stores) > 0:
        raise ValueError(f"该区域有关联的 {len(region.stores)} 个门店，无法删除")
    
    # 检查是否有子级区域
    if region.children and len(region.children) > 0:
        raise ValueError(f"该区域有 {len(region.children)} 个子级区域，无法删除")
    
    await db.delete(region)
    return True
