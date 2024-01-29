"""create order table

Revision ID: b7930b1e0c4a
Revises: acdd1da395cb
Create Date: 2024-01-04 15:58:22.905105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7930b1e0c4a'
down_revision: Union[str, None] = 'acdd1da395cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "order",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("userId", sa.Integer(), nullable=False),
        sa.Column("goods_reserved", sa.Boolean(), nullable=True),
        sa.Column("money_reserved", sa.Boolean(), nullable=True),
        sa.Column("courier_reserved", sa.Boolean(), nullable=True),
        sa.Column("reserv_user_canceled", sa.Boolean(), nullable=True),
        sa.Column("goods_fail", sa.Boolean(), nullable=True),
        sa.Column("money_fail", sa.Boolean(), nullable=True),
        sa.Column("courier_fail", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_id"), "order", ["id"], unique=True)
    op.create_index(op.f("ix_order_uuid"), "order", ["uuid"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_order_uuid"), table_name="order")
    op.drop_index(op.f("ix_order_id"), table_name="order")
    op.drop_table("order")
