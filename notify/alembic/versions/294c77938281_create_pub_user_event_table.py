"""create pub-user-event table

Revision ID: 294c77938281
Revises: 49fc84f49a6e
Create Date: 2024-02-14 13:47:25.111384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '294c77938281'
down_revision: Union[str, None] = '49fc84f49a6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pubuserevent",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("state", sa.Text(), nullable=True),
        sa.Column("delivered", sa.Boolean(), nullable=True),
        sa.Column("deliv_fail", sa.Boolean(), nullable=True),
        sa.Column("created_at", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.func.now(),
                  nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pub_user_event_id"), "pubuserevent", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_pub_user_event_id"), table_name="pubuserevent")
    op.drop_table("pubuserevent")

