"""
后台管理路由模块
处理系统统计、管理员用户、角色权限等后台管理接口
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.core.database import get_db
from app.core.deps import get_current_active_user, require_roles
from app.core.response import paginated, success
from app.models.user import User
from app.schemas.admin import (
    AdminUserCreateRequest,
    AdminUserListResponse,
    AdminUserResponse,
    AdminUserUpdateRequest,
    DashboardStatsResponse,
    ExportReportRequest,
    PermissionStructureResponse,
    RoleCreateRequest,
    RoleListResponse,
    RoleResponse,
    RoleUpdateRequest,
    SystemHealthResponse,
    SystemStatsResponse,
)
from app.services import admin_service, user_region_service

router = APIRouter(prefix="/admin", tags=["后台管理"])


@router.get("/dashboard/stats", summary="系统统计数据")
async def get_dashboard_stats(
    period: str = Query("30d", description="统计周期: 7d/30d/90d/all"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    获取仪表盘系统统计数据
    - 用户总数
    - 门店总数
    - 评论总数
    - 回复总数
    - 待审核数量
    - 活跃平台数
    """
    stats = await admin_service.get_system_stats(db, period)
    return success(data=stats)


@router.get("/system/health", summary="系统健康状态")
async def get_system_health(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    获取系统健康状态
    - 数据库连接状态
    - 缓存连接状态
    - 爬虫服务状态
    """
    health = await admin_service.get_system_health(db)
    return success(data=health)


@router.post("/system/export-report", summary="导出系统报告")
async def export_report(
    request: ExportReportRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """
    导出系统报告
    - 支持导出评论数据、审核数据、统计数据
    - 返回CSV格式文件
    """
    report_data = await admin_service.export_report(
        db, request.report_type, request.period
    )

    filename = f"report_{request.report_type}_{request.period}.csv"
    return StreamingResponse(
        iter([report_data]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/permissions/admins", summary="管理员列表")
async def get_admin_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    获取管理员用户列表
    """
    users, total = await admin_service.get_admin_users(db, page, page_size)
    items = []
    for user in users:
        d = AdminUserResponse.model_validate(user).model_dump(mode="json")
        d["assigned_stores"] = [str(s.store_id) for s in user.store_associations]
        items.append(d)
    return paginated(items=items, total=total, page=page, page_size=page_size)


@router.post("/permissions/admins", summary="新增管理员")
async def create_admin_user(
    request: AdminUserCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    创建新的管理员用户
    """
    user = await admin_service.create_admin_user(db, request)
    return success(
        data=AdminUserResponse.model_validate(user).model_dump(mode="json"),
        message="管理员创建成功",
    )


@router.put("/permissions/admins/{user_id}", summary="更新管理员")
async def update_admin_user(
    user_id: UUID,
    request: AdminUserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    更新管理员用户信息
    """
    user = await admin_service.update_admin_user(db, user_id, request)
    return success(
        data=AdminUserResponse.model_validate(user).model_dump(mode="json"),
        message="管理员更新成功",
    )


@router.post("/permissions/admins/{user_id}/disable", summary="禁用管理员")
async def disable_admin_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    禁用管理员用户
    """
    user = await admin_service.disable_admin_user(db, user_id)
    return success(
        data=AdminUserResponse.model_validate(user).model_dump(mode="json"),
        message="管理员已禁用",
    )


@router.get("/permissions/roles", summary="角色列表")
async def get_roles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    获取角色列表
    - 包含系统预定义角色和自定义角色
    """
    roles = await admin_service.get_roles(db)
    return success(
        data={
            "items": roles,
            "total": len(roles),
        }
    )


@router.post("/permissions/roles", summary="新增角色")
async def create_role(
    request: RoleCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    创建新角色
    """
    role = await admin_service.create_role(db, request)
    return success(data=role, message="角色创建成功")


@router.put("/permissions/roles/{role_id}", summary="更新角色")
async def update_role(
    role_id: UUID,
    request: RoleUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    更新角色信息
    - 系统角色不允许修改
    """
    role = await admin_service.update_role(db, role_id, request)
    return success(data=role, message="角色更新成功")


@router.get("/permissions/structure", summary="组织架构")
async def get_permissions_structure(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    获取权限组织架构
    - 按模块分类的权限列表
    """
    structure = await admin_service.get_permissions_structure(db)
    return success(data={"modules": structure})

@router.post("/permissions/admins/{user_id}/enable", summary="启用管理员")
async def enable_admin_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    启用管理员用户
    """
    user = await admin_service.enable_admin_user(db, user_id)
    return success(
        data=AdminUserResponse.model_validate(user).model_dump(mode="json"),
        message="管理员已启用",
    )


@router.delete("/permissions/admins/{user_id}", summary="删除管理员")
async def delete_admin_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    删除管理员用户（硬删除）
    """
    await admin_service.delete_admin_user(db, user_id)
    return success(message="管理员已删除")


@router.post("/permissions/admins/{user_id}/stores", summary="分配门店给用户")
async def assign_stores(
    user_id: UUID,
    body: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    分配门店给用户（更新 user_stores 表）
    - body: {"store_ids": ["uuid1", "uuid2", ...]}
    """
    store_ids = body.get("store_ids", [])
    store_uuids = [UUID(sid) for sid in store_ids]
    await admin_service.assign_stores(db, user_id, store_uuids)
    return success(message="门店分配成功")


@router.get("/permissions/admins/{user_id}/regions", summary="获取用户关联的区域")
async def get_user_regions(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    获取用户关联的区域列表
    """
    regions = await user_region_service.get_user_regions(db, user_id)
    return success(data={"items": regions})


@router.post("/permissions/admins/{user_id}/regions", summary="添加用户区域关联")
async def add_user_region(
    user_id: UUID,
    body: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    添加用户区域关联
    - body: {"region_id": "uuid"}
    """
    region_id = body.get("region_id")
    if not region_id:
        raise HTTPException(status_code=400, detail="缺少 region_id 参数")
    
    result = await user_region_service.add_user_region(db, user_id, UUID(region_id))
    return success(message=result["message"])


@router.delete("/permissions/admins/{user_id}/regions/{region_id}", summary="移除用户区域关联")
async def remove_user_region(
    user_id: UUID,
    region_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    移除用户区域关联
    """
    result = await user_region_service.remove_user_region(db, user_id, region_id)
    return success(message=result["message"])
