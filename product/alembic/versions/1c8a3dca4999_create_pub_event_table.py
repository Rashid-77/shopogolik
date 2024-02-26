"""create pub_event_table

Revision ID: 1c8a3dca4999
Revises: ce4aa0abe98c
Create Date: 2024-01-28 15:24:49.956186

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1c8a3dca4999"
down_revision: Union[str, None] = "ce4aa0abe98c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pubevent",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Text(), nullable=True),
        sa.Column("delivered", sa.Boolean(), nullable=True),
        sa.Column("deliv_fail", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pub_event_id"), "pubevent", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_pub_event_id"), table_name="pubevent")
    op.drop_table("pubevent")
