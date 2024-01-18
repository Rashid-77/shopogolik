"""create stock table

Revision ID: d4ecaa979d10
Revises: 97bc63e9a65d
Create Date: 2024-01-18 15:40:40.429916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4ecaa979d10'
down_revision: Union[str, None] = '97bc63e9a65d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stock",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("prod_id", sa.Integer(), nullable=False),
        sa.Column("updDate", 
                  sa.DateTime(timezone=True), 
                  server_default=sa.text("now()"), 
                  nullable=True),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stock_id"), "stock", ["id"], unique=True)
    op.create_index(op.f("ix_prod_id"), "stock", ["prod_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_prod_id"), table_name="stock")
    op.drop_index(op.f("ix_stock_id"), table_name="stock")
    op.drop_table("stock")
