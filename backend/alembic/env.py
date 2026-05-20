"""Alembic 环境配置 - 支持异步数据库迁移。"""

import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

# 将项目根目录添加到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# 导入应用配置和模型基类
from app.core.config import settings
from app.models.base import Base

# 导入所有模型以确保 Alembic 能正确发现
from app.models import (
    User, UserStore, Region,
    Store, StorePlatform,
    Review, ReplyAudit,
    AIModelConfig, AIPromptTemplate, AIRuleEngine, AIProcessingLog,
    NotificationChannel, NotificationRule, NotificationHistory, NotificationTemplate,
    SubscriptionPlan, UserSubscription,
    SpiderPlatform, SpiderSyncLog, SpiderTask,
    AnnualReport, WeeklyBrief, Competitor, CompetitorAnalysisTask,
    ReplyTemplate, AutoReplyConfig, UserNotificationSetting,
)

# Alembic Config 对象
config = context.config

# 配置日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 目标元数据
# 使用 Base.metadata 作为目标元数据，Alembic 将基于此生成迁移脚本
target_metadata = Base.metadata


def get_url():
    """获取数据库 URL。"""
    return str(settings.DATABASE_URL)


def get_sync_url():
    """获取同步数据库 URL（用于离线模式）。"""
    # 将 asyncpg 替换为 psycopg2 用于同步操作
    url = str(settings.DATABASE_URL)
    return url.replace("postgresql+asyncpg://", "postgresql://")


def run_migrations_offline() -> None:
    """以离线模式运行迁移。

    这种模式不使用引擎，而是直接使用连接字符串。
    适用于在没有数据库连接的情况下生成 SQL 脚本。
    """
    url = get_sync_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # 比较列类型变化
        compare_server_default=True,  # 比较默认值变化
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """执行迁移操作。"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """以异步模式运行迁移。"""
    # 构建配置字典
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """以在线模式运行迁移。

    这种模式创建数据库连接并执行迁移。
    使用异步引擎支持 asyncpg。
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
