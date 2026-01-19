"""create users table

Revision ID: cfa8b1b0d8c7
Revises: 652994e49809
Create Date: 2026-01-19 23:22:26.931418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfa8b1b0d8c7'
down_revision: Union[str, Sequence[str], None] = '652994e49809'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('email', sa.String(), unique=True, nullable=False),
                    sa.Column('password', sa.String(), unique=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
