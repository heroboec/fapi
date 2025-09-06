"""Users model added

Revision ID: e474a8ad7dbc
Revises: 5704497c1edb
Create Date: 2025-09-07 17:41:43.540025

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e474a8ad7dbc"
down_revision: Union[str, Sequence[str], None] = "5704497c1edb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
