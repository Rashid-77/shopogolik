"""create_balance_idempot_key_table

Revision ID: b3f9a3b3ef75
Revises: ee344ffc02dc
Create Date: 2024-02-04 14:22:39.160315

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b3f9a3b3ef75"
down_revision: Union[str, None] = "ee344ffc02dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "deposidemp",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.Text(), nullable=True, unique=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
    )
    op.create_index(op.f("ix_deposidemp_id"), "deposidemp", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_deposidemp_id"), table_name="deposidemp")
    op.drop_table("deposidemp")
