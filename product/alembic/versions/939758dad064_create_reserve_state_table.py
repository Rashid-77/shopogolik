"""create reserve_state table

Revision ID: 939758dad064
Revises: ee344ffc02dc
Create Date: 2024-01-31 12:09:03.264146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from models.reserve_log import ProdReserveState

# revision identifiers, used by Alembic.
revision: str = '939758dad064'
down_revision: Union[str, None] = 'ee344ffc02dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reserve",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_event_id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Text(), nullable=False),
        sa.Column("prod_id", sa.Integer(), nullable=False),
        sa.Column("to_reserve", sa.Integer(), nullable=False),
        sa.Column("cancel", sa.Boolean(), nullable=True),
        sa.Column("state", pgEnum(ProdReserveState), unique=False),
        sa.Column("amount_processed", sa.Integer(), nullable=False),
        sa.Column("updDate", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.text("now()"), 
                  nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reserve_id"), "reserve", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_reserve_id"), table_name="reserve")
    op.drop_table("reserve")
