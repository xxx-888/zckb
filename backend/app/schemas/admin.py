"""
后台管理相关 Schema
定义管理员用户、角色、系统统计等请求/响应数据结构
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class AdminUserResponse(BaseModel):
    """管理员用户响应"""

    id: UUID
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: str
    status: str
    last_login_at: Optional[datetime] = None
    created_at: datetime
    assigned_stores: list[str] = []

    model_config = {"from_attributes": True}


class AdminUserCreateRequest(BaseModel):
    """创建管理员用户请求"""

    username: str = Field(..., description="用户名", min_length=2, max_length=50)
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, description="手机号", min_length=11, max_length=11)
    password: str = Field(..., description="密码", min_length=6)
    role: str = Field(..., description="角色: HQ/OPERATOR/STORE")


class AdminUserUpdateRequest(BaseModel):
    """更新管理员用户请求"""

    username: Optional[str] = Field(None, description="用户名", min_length=2, max_length=50)
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, description="手机号", min_length=11, max_length=11)
    role: Optional[str] = Field(None, description="角色: HQ/OPERATOR/STORE")


class RoleResponse(BaseModel):
    """角色响应"""

    id: UUID
    name: str
    permissions: list[str]
    description: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class RoleCreateRequest(BaseModel):
    """创建角色请求"""

    name: str = Field(..., description="角色名称", min_length=1, max_length=50)
    permissions: list[str] = Field(default_factory=list, description="权限列表")
    description: Optional[str] = Field(None, description="角色描述")


class RoleUpdateRequest(BaseModel):
    """更新角色请求"""

    name: Optional[str] = Field(None, description="角色名称", max_length=50)
    permissions: Optional[list[str]] = Field(None, description="权限列表")
    description: Optional[str] = Field(None, description="角色描述")


class SystemStatsResponse(BaseModel):
    """系统统计响应"""

    total_users: int = 0
    total_stores: int = 0
    total_reviews: int = 0
    total_platforms: int = 0
    active_spiders: int = 0
    system_health: str = "healthy"


class DashboardStatsResponse(BaseModel):
    """仪表盘统计数据响应"""

    total_users: int = 0
    total_stores: int = 0
    total_reviews: int = 0
    total_replies: int = 0
    pending_audits: int = 0
    active_platforms: int = 0
    period: str = "30d"


class SystemHealthResponse(BaseModel):
    """系统健康状态响应"""

    status: str = "healthy"
    database: str = "connected"
    cache: str = "connected"
    spider_services: dict = {}
    timestamp: datetime


class AdminUserListResponse(BaseModel):
    """管理员用户列表响应"""

    items: list[AdminUserResponse]
    total: int
    page: int
    pageSize: int


class RoleListResponse(BaseModel):
    """角色列表响应"""

    items: list[RoleResponse]
    total: int


class PermissionItem(BaseModel):
    """权限项"""

    id: str
    name: str
    description: Optional[str] = None


class PermissionModule(BaseModel):
    """权限模块"""

    module: str
    name: str
    permissions: list[PermissionItem]


class PermissionStructureResponse(BaseModel):
    """权限组织架构响应"""

    modules: list[PermissionModule]


class ExportReportRequest(BaseModel):
    """导出报告请求"""

    report_type: str = Field(..., description="报告类型: reviews/audits/stats")
    period: str = Field("30d", description="时间周期: 7d/30d/90d/all")
