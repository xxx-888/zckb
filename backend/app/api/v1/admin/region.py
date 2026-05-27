"""Region Management API Routes -

提供区域管理的 CRUD 接口，仅管理员可访问
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_db
from app.core.deps import get_current_active_user, require_roles
from app.core.response import success, paginated
from app.models.user import User
from app.schemas.region import RegionCreate, RegionUpdate
from app.services import region_service

router = APIRouter(prefix="/admin/regions", tags=["管理员-区域管理"])


@router.get("", summary="获取区域列表（管理员）")
async def get_regions(
    parent_id: Optional[str] = Query(None, description="父级ID（None表示顶级）"),
    level: Optional[str] = Query(None, description="层级过滤"),
    tree: bool = Query(False, description="是否返回树形结构"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    获取区域列表
    
    - tree=true: 返回树形结构
    - parent_id: 指定父级ID（None表示顶级）
    - level: 按层级过滤（province/city/district）
    """
    if tree:
        tree_data = await region_service.get_region_tree(db)
        return success(data=tree_data)
    else:
        regions = await region_service.get_regions(
            db, parent_id=parent_id, level=level, tree=False
        )
        return success(data=regions)


@router.get("/tree", summary="获取区域树形结构（管理员）")
async def get_region_tree(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    获取区域树形结构
    """
    tree_data = await region_service.get_region_tree(db)
    return success(data=tree_data)


@router.get("/{region_id}", summary="获取单个区域详情（管理员）")
async def get_region(
    region_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    根据ID获取区域详情（包含父级和子级）
    """
    region = await region_service.get_region(db, region_id)
    if not region:
        return {"code": 404, "message": "区域不存在", "data": None}
    
    return success(data=region)


@router.post("", summary="创建区域（管理员）")
async def create_region(
    data: RegionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    创建新区域
    """
    region = await region_service.create_region(db, data)
    await db.commit()
    
    return success(
        data=region,
        message="创建成功",
    )


@router.put("/{region_id}", summary="更新区域（管理员）")
async def update_region(
    region_id: str,
    data: RegionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    更新区域信息
    """
    region = await region_service.update_region(db, region_id, data)
    if not region:
        return {"code": 404, "message": "区域不存在", "data": None}
    
    await db.commit()
    
    return success(
        data=region,
        message="更新成功",
    )


@router.delete("/{region_id}", summary="删除区域（管理员）")
async def delete_region(
    region_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    删除区域（有关联门店或子级区域时禁止删除）
    """
    try:
        success_flag = await region_service.delete_region(db, region_id)
        
        if not success_flag:
            return {"code": 404, "message": "区域不存在", "data": None}
        
        await db.commit()
        
        return success(message="删除成功")
    except ValueError as e:
        return {"code": 400, "message": str(e), "data": None}
