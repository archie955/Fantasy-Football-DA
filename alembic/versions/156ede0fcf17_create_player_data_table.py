"""create_player_data_table

Revision ID: 156ede0fcf17
Revises: 
Create Date: 2025-09-12 16:27:49.745798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '156ede0fcf17'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('players',
                    sa.Column('player_id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('team', sa.String(), nullable=False),
                    sa.Column('position', sa.String(), nullable=False),
                    sa.Column('passing_yards', sa.DECIMAL(10,3), nullable=False),
                    sa.Column('passing_touchdowns', sa.DECIMAL(10,3), nullable=False),
                    sa.Column('rushing_yards', sa.DECIMAL(10,3), nullable=False),
                    sa.Column('rushing_touchdowns', sa.DECIMAL(10,3), nullable=False),
                    sa.Column('fumbles_lost', sa.DECIMAL(10,3), nullable=False),
                    sa.Column('catches', sa.DECIMAL(10,3), nullable=False),
                    sa.Column('receiving_yards', sa.DECIMAL(10,3), nullable=False),
                    sa.Column('receiving_touchdowns', sa.DECIMAL(10,3), nullable=False),
                    sa.Column('fantasy_points_ppr', sa.DECIMAL(10,3), nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('players')
    pass
