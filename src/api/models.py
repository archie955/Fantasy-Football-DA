from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base

class Players(Base):
    __tablename__ = "players"

    name = Column(String, nullable=False)
    team = Column(String, nullable=False)
    catches = Column(DECIMAL(10,3), nullable=False)
    position = Column(String, nullable=False)
    player_id = Column(Integer, primary_key=True, nullable=False)
    fumbles_lost = Column(DECIMAL(10,3), nullable=False)
    passing_yards = Column(DECIMAL(10,3), nullable=False)
    rushing_yards = Column(DECIMAL(10,3), nullable=False)
    receiving_yards = Column(DECIMAL(10,3), nullable=False)
    fantasy_points_ppr = Column(DECIMAL(10,3), nullable=False)
    passing_touchdowns = Column(DECIMAL(10,3), nullable=False)
    rushing_touchdowns = Column(DECIMAL(10,3), nullable=False)
    receiving_touchdowns = Column(DECIMAL(10,3), nullable=False)



