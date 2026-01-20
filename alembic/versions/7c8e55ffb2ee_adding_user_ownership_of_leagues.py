"""adding user ownership of leagues

Revision ID: 7c8e55ffb2ee
Revises: cfa8b1b0d8c7
Create Date: 2026-01-20 16:51:49.817735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c8e55ffb2ee'
down_revision: Union[str, Sequence[str], None] = 'cfa8b1b0d8c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add column as nullable first
    op.add_column(
        'leagues',
        sa.Column('user_id', sa.Integer(), nullable=True)
    )

    # create foreign key
    op.create_foreign_key(
        'fk_leagues_user',
        'leagues',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # make existing league owned by me
    op.execute(
        "UPDATE leagues SET user_id = 1"
    )

    # now amke it not nullable
    op.alter_column(
        'leagues',
        'user_id',
        nullable=False
    )
    pass


def downgrade() -> None:
    op.drop_constraint('fk_leagues_user', 'leagues', type_='foreignkey')

    op.drop_column('leagues', 'user_id')
    pass
