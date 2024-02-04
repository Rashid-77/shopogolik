"""create_balance_table

Revision ID: b3f9a3b3ef75
Revises: ee344ffc02dc
Create Date: 2024-02-04 14:22:39.160315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3f9a3b3ef75'
down_revision: Union[str, None] = 'ee344ffc02dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "balance",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("balance", sa.DECIMAL(precision=9, scale=2), nullable=True),
        sa.Column("amount", sa.DECIMAL(precision=9, scale=2), nullable=True),
        sa.Column("depos_uuid", sa.Text(), nullable=True, unique=True),
        sa.Column("order_uuid", sa.Text(), nullable=True),
        sa.Column("deposit", sa.Boolean(), nullable=True),
        sa.Column("withdraw", sa.Boolean(), nullable=True),
        sa.Column("refunding", sa.Boolean(), nullable=True),
        sa.Column("updDate", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.func.now(), 
                  nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_balance_id"), "balance", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_balance_id"), table_name="balance")
    op.drop_table("balance")
