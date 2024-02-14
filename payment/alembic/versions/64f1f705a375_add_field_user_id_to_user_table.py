"""add field user_id to user table

Revision ID: 64f1f705a375
Revises: 3e51653c89b8
Create Date: 2024-02-13 13:52:31.848084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64f1f705a375'
down_revision: Union[str, None] = '3e51653c89b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user", sa.Column("user_id", sa.Integer(), nullable=False, server_default="0"))

def downgrade() -> None:
    op.drop_column("user", "user_id")
