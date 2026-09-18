"""add users table

Revision ID: 48fdf19672bb
Revises: a4133e663209
Create Date: 2026-09-18 00:26:25.621465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48fdf19672bb'
down_revision: Union[str, Sequence[str], None] = 'a4133e663209'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",sa.Column("id",sa.Integer(),primary_key=True,nullable=False),
                            sa.Column("email",sa.String(),unique=True,nullable=False),
                            sa.Column("password",sa.String(),nullable=False),
                            sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
