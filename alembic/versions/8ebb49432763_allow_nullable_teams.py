"""allow_nullable_teams

Revision ID: 8ebb49432763
Revises: 156ede0fcf17
Create Date: 2025-09-12 17:18:15.064781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ebb49432763'
down_revision: Union[str, Sequence[str], None] = '156ede0fcf17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('players', 'team', nullable=True)
    pass


def downgrade() -> None:
    op.alter_column('players', 'team', nullable=False)
    pass
