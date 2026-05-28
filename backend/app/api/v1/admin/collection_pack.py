"""
采集套餐后台管理路由
处理套餐 CRUD、订单管理（后台）
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_roles
from app.models.user import User
from app.schemas.collection_pack import (
    CollectionOrderResponse,
    CollectionPackCreateRequest,
    CollectionPackResponse,
    CollectionPackUpdateRequest,
    CreateCollectionOrderRequest,
)
from app.services.collection_pack_service import (
    create_pack,
    delete_pack,
    get_all_orders,
    get_pack_by_id,
    get_packs,
    update_order_status,
    update_pack,
)

router = APIRouter(prefix="/admin/collection-packs", tags=["采集套餐管理（后台）"])

# ==================== 套餐管理 ====================


@router.get("", response_model=list[CollectionPackResponse])
async def admin_get_packs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HQ")),
):
    """获取所有采集套餐（后台）"""
    packs = await get_packs(db, active_only=False)
    return [CollectionPackResponse.model_validate(p) for p in packs]


@router.post("", response_model=CollectionPackResponse)
async def admin_create_pack(
    data: CollectionPackCreateRequest,
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HQ")),
    db: AsyncSession = Depends(get_db),
):
    """新建采集套餐"""
    pack = await create_pack(db, data)
    return CollectionPackResponse.model_validate(pack)


@router.put("/{pack_id}", response_model=CollectionPackResponse)
async def admin_update_pack(
    pack_id: str,
    data: CollectionPackUpdateRequest,
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HQ")),
    db: AsyncSession = Depends(get_db),
):
    """更新采集套餐"""
    pack = await update_pack(db, pack_id, data)
    if not pack:
        from fastapi.exceptions import HTTPException
        raise HTTPException(status_code=404, detail="套餐不存在")
    return CollectionPackResponse.model_validate(pack)


@router.delete("/{pack_id}")
async def admin_delete_pack(
    pack_id: str,
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HQ")),
    db: AsyncSession = Depends(get_db),
):
    """删除采集套餐"""
    ok = await delete_pack(db, pack_id)
    if not ok:
        from fastapi.exceptions import HTTPException
        raise HTTPException(status_code=404, detail="套餐不存在")
    return {"message": "删除成功"}


# ==================== 订单管理 ====================


@router.get("/orders", response_model=list[CollectionOrderResponse])
async def admin_get_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: str = Query(None),
    status: str = Query(None),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HQ")),
    db: AsyncSession = Depends(get_db),
):
    """获取采集订单列表（后台）"""
    orders, total = await get_all_orders(
        db, user_id=user_id, status=status, page=page, page_size=page_size
    )
    return [CollectionOrderResponse(**o) for o in orders]


@router.put("/orders/{order_id}/status")
async def admin_update_order_status(
    order_id: str,
    new_status: str,
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HQ")),
    db: AsyncSession = Depends(get_db),
):
    """修改采集订单状态（后台）"""
    order = await update_order_status(db, order_id, new_status)
    if not order:
        from fastapi.exceptions import HTTPException
        raise HTTPException(status_code=404, detail="订单不存在")
    return {"message": "状态更新成功", "status": new_status}
