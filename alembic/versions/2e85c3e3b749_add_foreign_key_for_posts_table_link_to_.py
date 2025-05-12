"""add foreign key for posts table link to users table

Revision ID: 2e85c3e3b749
Revises: 5588762c065c
Create Date: 2025-05-12 17:04:23.285169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlmodel import ForeignKey


# revision identifiers, used by Alembic.
revision: str = '2e85c3e3b749'
down_revision: Union[str, None] = '5588762c065c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('Now()')) )
    op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users", 
                          local_cols=["user_id"], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_user_fk','posts')
    op.drop_column("posts", "user_id")
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
