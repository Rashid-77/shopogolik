"""add field created_at to user table

Revision ID: 4881f63c34b3
Revises: 64f1f705a375
Create Date: 2024-02-13 14:30:43.976219

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4881f63c34b3"
down_revision: Union[str, None] = "64f1f705a375"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("user", "created_at")
