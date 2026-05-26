"""
数据库连接与会话管理模块
使用 SQLAlchemy 异步引擎
"""

import json
import os
from datetime import datetime
from typing import AsyncGenerator
from uuid import UUID

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


def json_serializer(obj):
    """JSON序列化器，支持datetime和UUID"""
    return json.dumps(obj, default=_json_default)


def _json_default(obj):
    """json.dumps 的 default 回调，处理非标准类型"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


# 根据数据库类型创建引擎
if "sqlite" in os.environ.get("DATABASE_URL", "").lower():
    # SQLite
    async_engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,  # 生产环境关闭 SQL 日志
        connect_args={"check_same_thread": False},
        json_serializer=json_serializer,
    )

    # 为SQLite注册datetime和UUID类型适配器
    from sqlalchemy import String
    from sqlalchemy.dialects import sqlite as sqlite_dialect

    # 配置SQLite方言的类型默认值
    sqlite_dialect.NATIVE_NA = False
else:
    # PostgreSQL
    async_engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,  # 生产环境关闭 SQL 日志
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )

# 创建异步会话工厂
async_session_factory = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    数据库会话依赖注入
    用法: db: AsyncSession = Depends(get_db)
    自动管理事务的提交和回滚
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    初始化数据库，创建所有表
    在应用启动时调用
    """
    # 必须从 models.base 导入 Base，确保和模型使用的是同一个 Base 实例
    from app.models.base import Base
    
    # 导入所有模型以确保它们被注册到 Base.metadata
    import app.models.user
    import app.models.store
    import app.models.review
    import app.models.ai_config
    import app.models.notification
    import app.models.subscription
    import app.models.spider
    import app.models.report
    import app.models.settings as settings_models
    import app.models.verification_code  # 导入验证码模型
    import app.models.region  # 导入区域模型
    import app.models.user_region  # 导入用户-区域关联表
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    关闭数据库连接
    在应用关闭时调用
    """
    await async_engine.dispose()
