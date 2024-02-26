"""create_pub_event_table

Revision ID: f380c7f951b2
Revises: 2299ff5b3d1b
Create Date: 2024-02-07 12:12:11.536488

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f380c7f951b2"
down_revision: Union[str, None] = "2299ff5b3d1b"
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
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pub_event_id"), "pubevent", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_pub_event_id"), table_name="pubevent")
    op.drop_table("pubevent")
