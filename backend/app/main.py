"""
FastAPI 应用入口
创建应用实例，配置中间件、路由和生命周期事件
"""

import os

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 必须先设置 DATABASE_URL 和 JWT_SECRET_KEY 环境变量，供模型文件和 JWT 验证使用
from app.core.config import settings

os.environ["DATABASE_URL"] = settings.DATABASE_URL
os.environ["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY

from app.api.v1.router import api_router
from app.core.database import close_db, init_db
from app.core.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理：启动时初始化数据库，关闭时释放连接"""
    # 启动
    await init_db()
    yield
    # 关闭
    await close_db()


def create_app() -> FastAPI:
    """
    创建并配置 FastAPI 应用实例

    Returns:
        FastAPI: 配置完成的应用实例
    """
    app = FastAPI(
        title="CPA评价管理系统",
        description="餐饮商家评价管理平台API",
        version="1.0.0",
        lifespan=lifespan,
    )

    # 注册异常处理器
    register_exception_handlers(app)

    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由 - 添加 /api/v1 前缀
    app.include_router(api_router, prefix="/api/v1")

    return app


# 创建应用实例
app = create_app()
