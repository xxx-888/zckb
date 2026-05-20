"""
统一响应模型模块
提供标准化的 API 响应格式
"""

from typing import Generic, TypeVar

from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应模型"""

    code: int = 200
    message: str = "success"
    data: T | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应模型"""

    items: list[T]
    total: int
    page: int
    pageSize: int


def success(data: T | None = None, message: str = "success") -> dict:
    """
    构建成功响应

    Args:
        data: 响应数据
        message: 响应消息

    Returns:
        dict: 标准响应字典
    """
    return {
        "code": 200,
        "message": message,
        "data": data,
    }


def error(
    message: str = "请求失败",
    code: int = 400,
    status_code: int = 400,
) -> JSONResponse:
    """
    构建错误响应

    Args:
        message: 错误消息
        code: 业务错误码
        status_code: HTTP 状态码

    Returns:
        JSONResponse: FastAPI JSON 响应
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code,
            "message": message,
            "data": None,
        },
    )


def paginated(
    items: list[T],
    total: int,
    page: int,
    page_size: int,
) -> dict:
    """
    构建分页响应

    Args:
        items: 数据列表
        total: 总记录数
        page: 当前页码
        page_size: 每页大小

    Returns:
        dict: 分页响应字典
    """
    return {
        "code": 200,
        "message": "success",
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "pageSize": page_size,
        },
    }
