"""add foreign-key to posts table

Revision ID: 0b702d2a5002
Revises: 48fdf19672bb
Create Date: 2026-09-18 01:18:38.194505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b702d2a5002'
down_revision: Union[str, Sequence[str], None] = '48fdf19672bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("posts_users_fkey",source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("posts_users_fkey","posts")
    op.drop_column("posts","owner_id")
    pass
