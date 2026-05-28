"""
自定义异常模块
定义应用级别的异常类及 FastAPI 异常处理器
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """应用基础异常"""

    def __init__(
        self,
        message: str = "服务器内部错误",
        code: int = 500,
        status_code: int = 500,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AppException):
    """资源未找到异常 (404)"""

    def __init__(self, message: str = "资源未找到", code: int = 404) -> None:
        super().__init__(message=message, code=code, status_code=404)


class UnauthorizedException(AppException):
    """未授权异常 (401)"""

    def __init__(self, message: str = "未授权，请先登录", code: int = 401) -> None:
        super().__init__(message=message, code=code, status_code=401)


class ForbiddenException(AppException):
    """禁止访问异常 (403)"""

    def __init__(self, message: str = "权限不足，拒绝访问", code: int = 403) -> None:
        super().__init__(message=message, code=code, status_code=403)


class BusinessException(AppException):
    """业务逻辑异常 (400)"""

    def __init__(self, message: str = "业务处理失败", code: int = 400) -> None:
        super().__init__(message=message, code=code, status_code=400)


class SubscriptionRequiredException(AppException):
    """订阅过期/未订阅异常 (402)"""

    def __init__(self, message: str = "订阅已过期，请续费", code: int = 402) -> None:
        super().__init__(message=message, code=code, status_code=402)


class CreditInsufficientException(AppException):
    """采集积分不足异常 (402)"""

    def __init__(self, message: str = "采集积分不足", code: int = 402) -> None:
        super().__init__(message=message, code=code, status_code=402)


def register_exception_handlers(app: FastAPI) -> None:
    """
    注册全局异常处理器到 FastAPI 应用

    Args:
        app: FastAPI 应用实例
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        """处理所有 AppException 子类异常"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code,
                "message": exc.message,
                "data": None,
            },
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        """处理 ValueError（如 token 解码失败）"""
        return JSONResponse(
            status_code=401,
            content={
                "code": 401,
                "message": str(exc),
                "data": None,
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """处理未捕获的全局异常"""
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "服务器内部错误" if not settings.DEBUG else str(exc),
                "data": None,
            },
        )


# 避免循环导入，延迟导入 settings
from app.core.config import settings  # noqa: E402
