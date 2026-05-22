"""add owner_id to stores

Revision ID: 002
Revises: 001
Create Date: 2026-05-22 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = "002"
down_revision: str = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加 owner_id 列到 stores 表
    # SQLite 需要用 batch_alter_table
    with op.batch_alter_table("stores", schema=None) as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.String(36), nullable=True))
        batch_op.create_index("ix_stores_owner_id", ["owner_id"], unique=False)


def downgrade() -> None:
    with op.batch_alter_table("stores", schema=None) as batch_op:
        batch_op.drop_index("ix_stores_owner_id")
        batch_op.drop_column("owner_id")
