"""add user table

Revision ID: ddce070178ac
Revises: 4daee9cc7c7f
Create Date: 2024-04-01 15:01:31.524575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddce070178ac'
down_revision: Union[str, None] = '4daee9cc7c7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('email', sa.Integer(), nullable=False),
                            sa.Column('password', sa.Integer(), nullable=False),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')

    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
