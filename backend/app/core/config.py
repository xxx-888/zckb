"""
应用配置管理模块
使用 pydantic-settings 从环境变量和 .env 文件加载配置
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """应用全局配置"""

    # ---- 应用基础配置 ----
    APP_NAME: str = "CPA评价管理系统"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # ---- 数据库配置 ----
    # 从环境变量读取，支持 PostgreSQL / SQLite 切换
    # 格式: postgresql+asyncpg://user:pwd@host:5432/dbname
    DATABASE_URL: str = "sqlite+aiosqlite:///./cpa_review.db"
    DATABASE_URL_SYNC: str = "sqlite:///./cpa_review.db"

    # ---- Redis 配置 ----
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    @property
    def REDIS_URL(self) -> str:
        """构造 Redis URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # ---- JWT 配置 ----
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24小时

    # ---- CORS 配置 ----
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # ---- OpenAI 配置 ----
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o"

    # ---- 智谱 AI 配置 ----
    ZHIPU_API_KEY: str = ""
    ZHIPU_MODEL: str = "glm-4"

    # ---- DeepSeek 配置 ----
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # ---- 阿里云短信配置 ----
    ALIYUN_ACCESS_KEY_ID: str = ""
    ALIYUN_ACCESS_KEY_SECRET: str = ""
    ALIYUN_SMS_SIGN_NAME: str = ""
    ALIYUN_SMS_TEMPLATE_CODE_REGISTER: str = ""
    ALIYUN_SMS_TEMPLATE_CODE_RESET: str = ""
    ALIYUN_SMS_TEMPLATE_CODE_LOGIN: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# 全局配置单例
settings = Settings()
