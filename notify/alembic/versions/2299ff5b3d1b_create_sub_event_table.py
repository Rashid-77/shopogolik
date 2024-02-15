"""create_sub_event_table

Revision ID: 2299ff5b3d1b
Revises: 5cbac853b230
Create Date: 2024-02-07 12:12:05.113503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2299ff5b3d1b'
down_revision: Union[str, None] = '5cbac853b230'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subevent",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=True),
        sa.Column("order_id", sa.Text(), nullable=True),
        sa.Column("created_at", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.func.now(),
                  nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sub_event_id"), "subevent", ["id"], unique=True)



def downgrade() -> None:
    op.drop_index(op.f("ix_sub_event_id"), table_name="subevent")
    op.drop_table("subevent")
