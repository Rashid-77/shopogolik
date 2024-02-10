"""create product_reservation table

Revision ID: ce4aa0abe98c
Revises: d4ecaa979d10
Create Date: 2024-01-28 12:05:00.620232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce4aa0abe98c'
down_revision: Union[str, None] = 'd4ecaa979d10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "prodreserv",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("prod_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("updDate", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.text("now()"), 
                  nullable=True),
        sa.Column("state", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_prod_reserv_id"), "prodreserv", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_prod_reserv_id"), table_name="prodreserv")
    op.drop_table("prodreserv")
