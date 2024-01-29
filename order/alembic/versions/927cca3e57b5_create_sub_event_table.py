"""create sub_event_table

Revision ID: 927cca3e57b5
Revises: 7d5fba52cf9f
Create Date: 2024-01-28 13:34:10.369091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '927cca3e57b5'
down_revision: Union[str, None] = '7d5fba52cf9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subevent",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("updDate", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.text("now()"), 
                  nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sub_event_id"), "subevent", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_sub_event_id"), table_name="subevent")
    op.drop_table("subevent")
