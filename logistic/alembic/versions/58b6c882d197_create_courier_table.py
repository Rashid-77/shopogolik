"""create_courier_table

Revision ID: 58b6c882d197
Revises: acdd1da395cb
Create Date: 2024-02-06 10:36:26.612540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58b6c882d197'
down_revision: Union[str, None] = 'acdd1da395cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "courier",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("courier_id", 
                  sa.Integer(), 
                  sa.ForeignKey('User.id', ondelete='CASCADE'),
                  nullable=True ),
        sa.Column("from_t", sa.DateTime(timezone=True), nullable=True),
        sa.Column("to_t", sa.DateTime(timezone=True), nullable=True),
        sa.Column("order_uuid", sa.Text(), nullable=True),
        sa.Column("deliv_addr", sa.Text(), nullable=True),
        sa.Column("client_id", sa.Integer(), nullable=True ),
        sa.Column("reserve_uuid", sa.Integer, default=""),
        sa.Column("created_at", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.func.now(), 
                  nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_courier_id"), "courier", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_courier_id"), table_name="courier")
    op.drop_table("courier")
