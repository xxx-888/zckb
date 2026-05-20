"""
好评激活模块Schema定义
用于优质好评内容生成和授权相关接口的请求和响应模型
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class HighQualityReviewResponse(BaseModel):
    """优质好评响应模型"""

    id: UUID = Field(..., description="评论ID")
    user_name: Optional[str] = Field(None, description="用户昵称")
    avatar: Optional[str] = Field(None, description="用户头像")
    content: Optional[str] = Field(None, description="评论内容")
    rating: int = Field(..., description="评分")
    has_image: bool = Field(..., description="是否有图片")
    length: int = Field(..., description="内容长度")
    sentiment: str = Field(..., description="情感倾向")
    authorized: bool = Field(..., description="是否已授权")
    suggested_script: Optional[str] = Field(None, description="建议话术")
    created_at: datetime = Field(..., description="评论时间")


class BrandScriptResponse(BaseModel):
    """品牌话术响应模型"""

    id: UUID = Field(..., description="话术ID")
    name: str = Field(..., description="话术名称")
    content: str = Field(..., description="话术内容")
    category: str = Field(..., description="分类")
    usage_count: int = Field(..., description="使用次数")


class GenerateContentRequest(BaseModel):
    """生成内容请求模型"""

    review_id: UUID = Field(..., description="评论ID")
    platform: str = Field(..., description="目标平台: xiaohongshu/douyin/weibo")


class GeneratedContentResponse(BaseModel):
    """生成内容响应模型"""

    review_id: UUID = Field(..., description="评论ID")
    content: str = Field(..., description="生成的内容")
    platform: str = Field(..., description="目标平台")
    hashtags: list[str] = Field(..., description="推荐话题标签")
