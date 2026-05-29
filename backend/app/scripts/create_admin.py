"""
创建超级管理员账户脚本
用法：
  python -m app.scripts.create_admin
  python -m app.scripts.create_admin --username admin --password 123456 --email admin@example.com
"""
import asyncio
import sys
import os

# 必须在导入 app 之前设置环境变量
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://admin:TvOEExy25T9jh4d1@47.108.137.126:5432/zctest")
os.environ.setdefault("JWT_SECRET_KEY", "dev-jwt-secret-key-do-not-use-in-production")

from app.core.security import get_password_hash
from app.core.database import async_engine, async_session_factory
from app.models.user import User


async def create_admin(username: str, password: str, email: str = None, phone: str = None):
    async with async_session_factory() as db:
        # 检查是否已存在
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.username == username))
        existing = result.scalar_one_or_none()
        if existing:
            print(f"管理员账户已存在: {username} (id={existing.id})")
            return existing

        user = User(
            username=username,
            hashed_password=get_password_hash(password),
            email=email,
            phone=phone,
            role="SUPER_ADMIN",
            status="active",
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)
        await db.commit()
        print(f"[成功] 超级管理员创建成功！")
        print(f"   ID:       {user.id}")
        print(f"   用户名:   {user.username}")
        print(f"   角色:     {user.role}")
        print(f"   状态:     {user.status}")
        return user


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="创建超级管理员账户")
    parser.add_argument("--username", default="admin", help="用户名 (默认: admin)")
    parser.add_argument("--password", default="admin123", help="密码 (默认: admin123)")
    parser.add_argument("--email", default=None, help="邮箱")
    parser.add_argument("--phone", default=None, help="手机号")
    args = parser.parse_args()

    print(f"正在创建管理员账户: {args.username}")
    asyncio.run(create_admin(args.username, args.password, args.email, args.phone))
