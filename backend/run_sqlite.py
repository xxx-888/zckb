#!/usr/bin/env python3
"""
SQLite 开发环境启动脚本
无需 PostgreSQL 即可快速启动后端服务
"""

import os
import sys

# 设置环境变量使用 SQLite
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./review_platform.db"
os.environ["DATABASE_URL_SYNC"] = "sqlite:///./review_platform.db"

# 导入并运行主应用
from app.main import app
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 CPA评价管理系统 - SQLite 开发环境")
    print("=" * 60)
    print("\n📋 环境信息:")
    print("  - 数据库: SQLite (./review_platform.db)")
    print("  - API地址: http://localhost:8000")
    print("  - API文档: http://localhost:8000/docs")
    print("  - 前端地址: http://localhost:5173")
    print("\n⚠️  注意: 这是开发环境，生产环境请使用 PostgreSQL")
    print("=" * 60)
    print()

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
