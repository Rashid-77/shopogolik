"""create sub_prod_event_table

Revision ID: 927cca3e57b5
Revises: 7d5fba52cf9f
Create Date: 2024-01-28 13:34:10.369091

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "927cca3e57b5"
down_revision: Union[str, None] = "7d5fba52cf9f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subprodevent",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sub_prod_event_id"), "subprodevent", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_sub_prod_event_id"), table_name="subprodevent")
    op.drop_table("subprodevent")
