"""数据库迁移：创建 payment_records 表"""
from app.models.base import Base
from app.models.subscription import PaymentRecord
from sqlalchemy import create_engine

# 使用 SQLite 数据库
engine = create_engine("sqlite:///./zc.db")

# 只创建 payment_records 表
Base.metadata.create_all(engine, tables=[Base.metadata.tables["payment_records"]])

print("payment_records 表创建成功！")
