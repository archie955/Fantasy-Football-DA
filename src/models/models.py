from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Table, TIMESTAMP, text
from sqlalchemy.orm import relationship
from src.database.database import Base

team_players = Table(
    "team_players",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True),
    Column("player_id", Integer, ForeignKey("projections.id", ondelete="CASCADE"), primary_key=True),
)

class PlayerProjections(Base):
    __tablename__ = "projections"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    team = Column(String, nullable=False)
    position = Column(String, nullable=False)
    fantasy_points_ppr = Column(DECIMAL(10,3), nullable=False)

    # Many-to-many relationship with Teams
    teams = relationship("Teams", secondary=team_players, back_populates="players")


class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    teams = relationship("Teams", back_populates="league", cascade="all, delete-orphan")


class Teams(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)   # Team name chosen by owner
    league_id = Column(Integer, ForeignKey("leagues.id", ondelete="CASCADE"), nullable=False)

    league = relationship("League", back_populates="teams")
    players = relationship("PlayerProjections", secondary=team_players, back_populates="teams")


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))