"""create sub-user-event table

Revision ID: 21010e96f565
Revises: 294c77938281
Create Date: 2024-02-14 13:47:31.726116

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "21010e96f565"
down_revision: Union[str, None] = "294c77938281"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subuserevent",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("state", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sub_user_event_id"), "subuserevent", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_sub_user_event_id"), table_name="subuserevent")
    op.drop_table("subuserevent")
