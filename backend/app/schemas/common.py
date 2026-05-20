"""
通用 Schema
定义分页参数、ID 请求等通用数据结构
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """分页参数"""

    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")


class IdRequest(BaseModel):
    """ID 请求"""

    id: UUID = Field(..., description="记录ID")
