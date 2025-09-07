"""Add unique to users email.

Revision ID: ea83223bb0a4
Revises: e474a8ad7dbc
Create Date: 2025-09-07 18:08:09.630362

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ea83223bb0a4"
down_revision: Union[str, Sequence[str], None] = "e474a8ad7dbc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
