"""create user table

Revision ID: acdd1da395cb
Revises:
Create Date: 2023-10-30 17:59:19.741947

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "acdd1da395cb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "User",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("disabled", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "User", ["email"], unique=True)
    op.create_index(op.f("ix_user_full_name"), "User", ["username"], unique=False)
    op.create_index(op.f("ix_user_id"), "User", ["id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_user_email"), table_name="User")
    op.drop_index(op.f("ix_user_full_name"), table_name="User")
    op.drop_index(op.f("ix_user_id"), table_name="User")
    op.drop_table("User")
