"""create sub_event_table

Revision ID: ee344ffc02dc
Revises: 1c8a3dca4999
Create Date: 2024-01-28 15:25:03.259141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee344ffc02dc'
down_revision: Union[str, None] = '1c8a3dca4999'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subevent",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=True),
        sa.Column("order_id", sa.Text(), nullable=True),
        sa.Column("updDate", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.func.now(),
                  nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sub_event_id"), "subevent", ["id"], unique=True)



def downgrade() -> None:
    op.drop_index(op.f("ix_sub_event_id"), table_name="subevent")
    op.drop_table("subevent")
