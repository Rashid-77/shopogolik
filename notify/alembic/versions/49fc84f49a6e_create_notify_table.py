"""create_notify_table

Revision ID: 49fc84f49a6e
Revises: f380c7f951b2
Create Date: 2024-02-11 16:05:09.945465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49fc84f49a6e'
down_revision: Union[str, None] = 'f380c7f951b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notify",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_uuid", sa.Uuid(), nullable=True),
        sa.Column("client_id", 
                  sa.Integer(), 
                  sa.ForeignKey('User.id', ondelete='CASCADE'),
                  nullable=True),
        sa.Column("msg", sa.Text(), nullable=True),
        sa.Column("delivered", sa.Boolean(), nullable=True),
        sa.Column("created_at", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.func.now(),
                  nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_notify_id"), "notify", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_notify_id"), table_name="notify")
    op.drop_table("notify")
