"""
添加 payment_records 表的 billing_cycle 字段
"""
from sqlalchemy import text


def upgrade(session):
    """执行迁移"""
    session.execute(text("""
        ALTER TABLE payment_records 
        ADD COLUMN billing_cycle VARCHAR(20) NOT NULL DEFAULT 'yearly' 
        COMMENT '计费周期: monthly/yearly'
    """))
    session.commit()
    print("✅ 已添加 billing_cycle 字段到 payment_records 表")


def downgrade(session):
    """回滚迁移"""
    session.execute(text("""
        ALTER TABLE payment_records 
        DROP COLUMN billing_cycle
    """))
    session.commit()
    print("✅ 已回滚 billing_cycle 字段")
