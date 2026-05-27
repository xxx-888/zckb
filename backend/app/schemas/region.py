"""Region schemas - 区域管理 Pydantic 模型"""

from pydantic import BaseModel, Field, field_validator, model_serializer
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID


class RegionBase(BaseModel):
    """区域基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="区域名称")
    parent_id: Optional[str] = Field(None, description="父级区域ID")
    level: str = Field(..., description="层级: province-省, city-市, district-区")
    code: Optional[str] = Field(None, max_length=20, description="行政区划代码")


class RegionCreate(RegionBase):
    """创建区域"""
    pass


class RegionUpdate(BaseModel):
    """更新区域（所有字段可选）"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    parent_id: Optional[str] = Field(None, description="设置为空字符串''表示清除父级")
    level: Optional[str] = Field(None)
    code: Optional[str] = Field(None, max_length=20)


class RegionResponse(RegionBase):
    """区域响应模型"""
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # 关系字段（使用字典，避免SQLAlchemy对象序列化问题）
    parent: Optional[dict] = None
    children: List[dict] = []
    store_count: int = 0  # 关联的门店数量
    
    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        """将UUID转换为字符串"""
        if isinstance(v, UUID):
            return str(v)
        return v
    
    @field_validator('parent_id', mode='before')
    @classmethod
    def validate_parent_id(cls, v):
        """将UUID转换为字符串"""
        if isinstance(v, UUID):
            return str(v)
        return v
    
    @field_validator('parent', mode='before')
    @classmethod
    def validate_parent(cls, v):
        """将SQLAlchemy对象转换为字典"""
        if v is None:
            return None
        if isinstance(v, dict):
            return v
        # 假设v是SQLAlchemy对象
        return {
            "name": v.name,
            "level": v.level,
            "code": v.code
        }
    
    @field_validator('children', mode='before')
    @classmethod
    def validate_children(cls, v):
        """将SQLAlchemy对象列表转换为字典列表"""
        if not v:
            return []
        if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
            return v
        # 假设v是SQLAlchemy对象列表
        return [
            {
                "id": str(child.id) if isinstance(child.id, UUID) else child.id,
                "name": child.name,
                "level": child.level,
                "code": child.code
            }
            for child in v
        ]
    
    class Config:
        from_attributes = True


class RegionTreeResponse(BaseModel):
    """区域树形结构响应"""
    id: str
    name: str
    level: str
    code: Optional[str] = None
    children: List["RegionTreeResponse"] = []
    
    @field_validator('id', mode='before')
    @classmethod
    def validate_tree_id(cls, v):
        """将UUID转换为字符串"""
        if isinstance(v, UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True
