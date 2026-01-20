"""update all tables

Revision ID: 5035ff547bf0
Revises: 7c8e55ffb2ee
Create Date: 2026-01-20 17:31:14.344807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5035ff547bf0'
down_revision: Union[str, Sequence[str], None] = '7c8e55ffb2ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    # -------------------------
    # USERS TABLE FIX
    # -------------------------

    # Drop password unique constraint if exists
    # Constraint name may differ — adjust if needed
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint("users_password_key", type_="unique")


    # -------------------------
    # TEAMS TABLE
    # -------------------------

    # add user_id nullable first
    op.add_column(
        "teams",
        sa.Column("user_id", sa.Integer(), nullable=True)
    )

    # make it foreign key to users
    op.create_foreign_key(
        "fk_teams_user",
        "teams",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )

    # backfill teams.user_id from leagues
    connection.execute(
        sa.text("""
            UPDATE teams
            SET user_id = leagues.user_id
            FROM leagues
            WHERE teams.league_id = leagues.id
        """)
    )

    # make it NOT NULL
    op.alter_column(
        "teams",
        "user_id",
        nullable=False
    )

    # add indexes
    op.create_index("ix_teams_user_id", "teams", ["user_id"])
    op.create_index("ix_teams_league_id", "teams", ["league_id"])

    # add composite uniqueness
    op.create_unique_constraint(
        "uq_league_team",
        "teams",
        ["league_id", "name"]
    )


    # -------------------------
    # TEAM_PLAYERS TABLE
    # -------------------------

    # add user_id and league_id nullable first
    op.add_column(
        "team_players",
        sa.Column("user_id", sa.Integer(), nullable=True)
    )
    op.add_column(
        "team_players",
        sa.Column("league_id", sa.Integer(), nullable=True)
    )

    # create foreign keys
    op.create_foreign_key(
        "fk_team_players_user",
        "team_players",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )
    op.create_foreign_key(
        "fk_team_players_league",
        "team_players",
        "leagues",
        ["league_id"],
        ["id"],
        ondelete="CASCADE"
    )

    # backfill ownership from teams
    connection.execute(
        sa.text("""
            UPDATE team_players
            SET user_id = teams.user_id
            FROM teams
            WHERE team_players.team_id = teams.id
        """)
    )
    connection.execute(
        sa.text("""
            UPDATE team_players
            SET league_id = teams.league_id
            FROM teams
            WHERE team_players.team_id = teams.id
        """)
    )

    # make NOT NULL
    op.alter_column(
        "team_players",
        "user_id",
        nullable=False
    )
    op.alter_column(
        "team_players",
        "league_id",
        nullable=False
    )

    # 5. Add indexes
    op.create_index("ix_team_players_team_id", "team_players", ["team_id"])
    op.create_index("ix_team_players_player_id", "team_players", ["player_id"])
    op.create_index("ix_team_players_user_id", "team_players", ["user_id"])
    op.create_index("ix_team_players_league_id", "team_players", ["league_id"])


    # -------------------------
    # LEAGUES INDEX (if missing)
    # -------------------------

    op.create_index(
        "ix_leagues_user_id",
        "leagues",
        ["user_id"]
    )


    # -------------------------
    # PROJECTIONS INDEXES
    # -------------------------

    op.create_index("ix_players_name", "projections", ["name"])
    op.create_index("ix_players_team", "projections", ["team"])
    op.create_index("ix_players_position", "projections", ["position"])

    pass


def downgrade() -> None:
    # -------------------------
    # PROJECTIONS
    # -------------------------

    op.drop_index("ix_players_position", table_name="projections")
    op.drop_index("ix_players_team", table_name="projections")
    op.drop_index("ix_players_name", table_name="projections")


    # -------------------------
    # TEAM_PLAYERS
    # -------------------------

    op.drop_index("ix_team_players_league_id", table_name="team_players")
    op.drop_index("ix_team_players_user_id", table_name="team_players")
    op.drop_index("ix_team_players_player_id", table_name="team_players")
    op.drop_index("ix_team_players_team_id", table_name="team_players")

    op.drop_constraint("fk_team_players_user", "team_players", type_="foreignkey")
    op.drop_constraint("fk_team_players_league", "team_players", type="foreignkey")

    op.drop_column("team_players", "user_id")
    op.drop_column("team_players", "league_id")


    # -------------------------
    # TEAMS
    # -------------------------

    op.drop_constraint("uq_league_team", "teams", type_="unique")

    op.drop_index("ix_teams_league_id", table_name="teams")
    op.drop_index("ix_teams_user_id", table_name="teams")

    op.drop_constraint("fk_teams_user", "teams", type_="foreignkey")

    op.drop_column("teams", "user_id")


    # -------------------------
    # LEAGUES
    # -------------------------

    op.drop_index("ix_leagues_user_id", table_name="leagues")


    # -------------------------
    # USERS
    # -------------------------

    with op.batch_alter_table("users") as batch_op:
        batch_op.create_unique_constraint(
            "users_password_key",
            ["password"]
        )
    pass
