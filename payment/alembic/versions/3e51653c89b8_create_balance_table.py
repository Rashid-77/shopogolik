"""create_balance_table

Revision ID: 3e51653c89b8
Revises: b3f9a3b3ef75
Create Date: 2024-02-05 16:03:32.885386

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3e51653c89b8"
down_revision: Union[str, None] = "b3f9a3b3ef75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "balance",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("balance", sa.DECIMAL(precision=9, scale=2), nullable=True),
        sa.Column("amount", sa.DECIMAL(precision=9, scale=2), nullable=True),
        sa.Column("deposit", sa.Boolean(), nullable=True),
        sa.Column("reserve", sa.Boolean(), nullable=True),
        sa.Column("withdraw", sa.Boolean(), nullable=True),
        sa.Column("refunding", sa.Boolean(), nullable=True),
        sa.Column("success", sa.Boolean(), nullable=True),
        sa.Column(
            "deposidemp_id",
            sa.Integer(),
            sa.ForeignKey("deposidemp.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("order_uuid", sa.Text(), nullable=True),
        sa.Column("reserve_uuid", sa.Text(), nullable=True),
        sa.Column("withdraw_uuid", sa.Text(), nullable=True),
        sa.Column("refund_uuid", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_balance_id"), "balance", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_balance_id"), table_name="balance")
    op.drop_table("balance")
