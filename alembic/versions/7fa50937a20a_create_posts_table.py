"""create posts table

Revision ID: 7fa50937a20a
Revises: 
Create Date: 2024-04-01 00:53:23.106365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fa50937a20a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.INTEGER(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')