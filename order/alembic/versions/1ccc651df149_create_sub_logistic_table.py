"""create_sub_logistic_table

Revision ID: 1ccc651df149
Revises: 8f368c482cdf
Create Date: 2024-02-07 15:22:57.952784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ccc651df149'
down_revision: Union[str, None] = '8f368c482cdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sublogisevent",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Text(), nullable=True),
        sa.Column("created_at", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.func.now(),
                  nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sub_logistic_event_id"), "sublogisevent", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_sub_logistic_event_id"), table_name="sublogisevent")
    op.drop_table("sublogisevent")
