"""add coontent column to posts table

Revision ID: 4daee9cc7c7f
Revises: 7fa50937a20a
Create Date: 2024-04-01 14:49:02.815516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4daee9cc7c7f'
down_revision: Union[str, None] = '7fa50937a20a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
