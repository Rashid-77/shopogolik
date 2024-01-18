"""create product table

Revision ID: 97bc63e9a65d
Revises: b7930b1e0c4a
Create Date: 2024-01-17 10:29:21.960115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97bc63e9a65d'
down_revision: Union[str, None] = 'b7930b1e0c4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sku", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.DECIMAL(8, 2), nullable=False),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.Column("width_m", sa.Float(), nullable=True),
        sa.Column("length_m", sa.Float(), nullable=True),
        sa.Column("height_m", sa.Float(), nullable=True),
        sa.Column("volume_m3", sa.Float(), nullable=True),
        sa.Column("carDescr", sa.String(), nullable=True),
        sa.Column("shortDescr", sa.String(), nullable=True),
        sa.Column("longDescr", sa.String(), nullable=True),
        sa.Column("thumb", sa.String(), nullable=True),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("updDate", sa.Date(), nullable=True),
        sa.Column("live", sa.Boolean(), nullable=True),
        sa.Column("virtual", sa.Boolean(), nullable=True),
        sa.Column("unlimited", sa.Boolean(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_product_id"), "product", ["id"], unique=True)
    op.create_index(op.f("ix_name_id"), "product", ["name"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_name_id"), table_name="product")
    op.drop_index(op.f("ix_product_id"), table_name="product")
    op.drop_table("product")
