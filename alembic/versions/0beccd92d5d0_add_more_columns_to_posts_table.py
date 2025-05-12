"""add more columns to posts table

Revision ID: 0beccd92d5d0
Revises: d0e3aea848f8
Create Date: 2025-05-12 16:37:11.581564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0beccd92d5d0'
down_revision: Union[str, None] = 'd0e3aea848f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',  sa.Column('content', sa.String(), nullable=False))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')

