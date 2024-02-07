"""create sub_paym_event table

Revision ID: 8f368c482cdf
Revises: 927cca3e57b5
Create Date: 2024-01-29 21:24:18.352703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f368c482cdf'
down_revision: Union[str, None] = '927cca3e57b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subpaymevent",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("updDate", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.func.now(),
                  nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sub_paym_event_id"), "subpaymevent", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_sub_paym_event_id"), table_name="subpaymevent")
    op.drop_table("subpaymevent")