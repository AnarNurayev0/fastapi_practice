"""add content column to posts table

Revision ID: a4133e663209
Revises: e459e3af1174
Create Date: 2026-09-18 00:23:40.829035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4133e663209'
down_revision: Union[str, Sequence[str], None] = 'e459e3af1174'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","content")
    pass
