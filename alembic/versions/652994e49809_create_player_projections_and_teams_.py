"""create_player_projections_and_teams_tables

Revision ID: 652994e49809
Revises: 8ebb49432763
Create Date: 2025-09-13 13:15:26.156704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '652994e49809'
down_revision: Union[str, Sequence[str], None] = '8ebb49432763'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create projections (players) table
    op.create_table(
        "projections",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("team", sa.String(), nullable=False),
        sa.Column("position", sa.String(), nullable=False),
        sa.Column("fantasy_points_ppr", sa.DECIMAL(10, 3), nullable=False),
    )

    op.create_table(
        "leagues",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), unique=True, nullable=False),
    )

    # Create teams table
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("league_id", sa.Integer, sa.ForeignKey("leagues.id", ondelete="CASCADE")),
    )

    # Association table for many-to-many relationship
    op.create_table(
        "team_players",
        sa.Column("team_id", sa.Integer, sa.ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("player_id", sa.Integer, sa.ForeignKey("projections.id", ondelete="CASCADE"), primary_key=True),
    )
    pass


def downgrade() -> None:
    op.drop_table("team_players")
    op.drop_table("teams")
    op.drop_table("leagues")
    op.drop_table("projections")
    pass
