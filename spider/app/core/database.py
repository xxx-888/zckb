"""数据库连接管理模块。"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

# 声明式基类
Base = declarative_base()


class DatabaseManager:
    """数据库管理器。
    
    管理异步数据库连接池和会话。
    """
    
    def __init__(self) -> None:
        """初始化数据库管理器。"""
        self.engine = None
        self.async_session_maker = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """初始化数据库连接池。"""
        if self._initialized:
            return
        
        try:
            self.engine = create_async_engine(
                settings.database_url,
                pool_size=settings.db_pool_size,
                max_overflow=settings.db_max_overflow,
                pool_timeout=settings.db_pool_timeout,
                echo=settings.log_level == "DEBUG",
            )
            
            self.async_session_maker = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
            )
            
            self._initialized = True
            logger.info("Database connection pool initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    async def close(self) -> None:
        """关闭数据库连接池。"""
        if self.engine:
            await self.engine.dispose()
            self._initialized = False
            logger.info("Database connection pool closed")
    
    async def create_tables(self) -> None:
        """创建所有表（用于开发环境）。"""
        if not self.engine:
            raise RuntimeError("Database not initialized")
        
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created")
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取数据库会话上下文管理器。
        
        Yields:
            AsyncSession: 异步数据库会话
        """
        if not self.async_session_maker:
            raise RuntimeError("Database not initialized")
        
        session = self.async_session_maker()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取数据库会话（用于FastAPI依赖注入）。
        
        Yields:
            AsyncSession: 异步数据库会话
        """
        if not self.async_session_maker:
            raise RuntimeError("Database not initialized")
        
        session = self.async_session_maker()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()


# 全局数据库管理器实例
db_manager = DatabaseManager()


# 便捷函数
async def init_db() -> None:
    """初始化数据库。"""
    await db_manager.initialize()


async def close_db() -> None:
    """关闭数据库连接。"""
    await db_manager.close()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话生成器。"""
    async with db_manager.session() as session:
        yield session
