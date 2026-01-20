from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Table, TIMESTAMP, text, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from src.database.database import Base

team_players = Table(
    "team_players",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True),
    Column("league_id", Integer, ForeignKey("leagues.id", ondelete="CASCADE"), primary_key=True, index=True),
    Column("team_id", Integer, ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True, index=True),
    Column("player_id", Integer, ForeignKey("projections.id", ondelete="CASCADE"), primary_key=True),
)

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    leagues = relationship("League", back_populates="owner", cascade="all, delete-orphan")



class League(Base):
    __tablename__ = "leagues"

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_league"),
    ) # this constraint allows for name duplicates across users, but not within a particular users leagues.

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)

    owner = relationship("Users", back_populates="leagues")

    teams = relationship("Teams", back_populates="league", cascade="all, delete-orphan")


class Team(Base):
    __tablename__ = "teams"

    __table_args__ = (
        UniqueConstraint("league_id", "name", name="uq_league_team"),
        Index("ix_teams_user_id", "user_id"),
        Index("ix_teams_league_id", "league_id"),
    ) # this constraint prevents duplicate team names within a given league

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)   # Team name chosen by owner
    league_id = Column(Integer, ForeignKey("leagues.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    league = relationship("League", back_populates="teams")
    players = relationship("PlayerProjections", secondary=team_players, back_populates="teams")




class PlayerProjections(Base):
    __tablename__ = "projections"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    team = Column(String, nullable=False)
    position = Column(String, nullable=False)
    fantasy_points_ppr = Column(DECIMAL(10,3), nullable=False)

    # Many-to-many relationship with Teams
    teams = relationship("Team", secondary=team_players, back_populates="players")



