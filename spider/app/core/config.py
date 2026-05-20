"""
Application configuration management using Pydantic Settings.
"""
from functools import lru_cache
from typing import Optional

from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Redis Configuration
    redis_url: RedisDsn = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL for general use",
    )
    celery_broker_url: RedisDsn = Field(
        default="redis://localhost:6379/1",
        description="Redis URL for Celery message broker",
    )
    celery_result_backend: RedisDsn = Field(
        default="redis://localhost:6379/2",
        description="Redis URL for Celery result backend",
    )

    # Main Backend API Configuration
    api_base_url: str = Field(
        default="http://localhost:8000/api/v1",
        description="Main backend API base URL",
    )
    api_key: str = Field(
        default="",
        description="API key for authentication with main backend",
    )

    # Task Configuration
    max_concurrent_tasks: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Maximum number of concurrent spider tasks",
    )
    task_timeout: int = Field(
        default=300,
        ge=30,
        le=3600,
        description="Task timeout in seconds",
    )

    # Playwright Configuration
    playwright_headless: bool = Field(
        default=True,
        description="Run browser in headless mode",
    )
    playwright_slow_mo: int = Field(
        default=0,
        ge=0,
        le=10000,
        description="Slow down Playwright operations by specified milliseconds",
    )
    playwright_browser_type: str = Field(
        default="chromium",
        pattern="^(chromium|firefox|webkit)$",
        description="Browser type for Playwright",
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Logging level",
    )

    # Database
    database_url: Optional[str] = Field(
        default=None,
        description="Database URL for local task queue storage",
    )

    # Platform Credentials (optional, can be passed per-task)
    meituan_username: Optional[str] = None
    meituan_password: Optional[str] = None
    douyin_username: Optional[str] = None
    douyin_password: Optional[str] = None
    taobao_username: Optional[str] = None
    taobao_password: Optional[str] = None
    jd_username: Optional[str] = None
    jd_password: Optional[str] = None

    @property
    def celery_config(self) -> dict:
        """Generate Celery configuration dictionary."""
        return {
            "broker_url": str(self.celery_broker_url),
            "result_backend": str(self.celery_result_backend),
            "task_serializer": "json",
            "accept_content": ["json"],
            "result_serializer": "json",
            "timezone": "Asia/Shanghai",
            "enable_utc": True,
            "task_track_started": True,
            "task_time_limit": self.task_timeout * 2,
            "task_soft_time_limit": self.task_timeout,
            "worker_prefetch_multiplier": 1,
            "worker_concurrency": self.max_concurrent_tasks,
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
