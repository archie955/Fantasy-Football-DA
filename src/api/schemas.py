from pydantic import BaseModel
from typing import Optional, List

class FetchData(BaseModel):
    player_id: int
    name: str
    team: str
    position: str
    passing_yards: float
    passing_touchdowns: float
    rushing_yards: float
    rushing_touchdowns: float
    fumbles_lost: float
    catches: float
    receiving_yards: float
    receiving_touchdowns: float
    fantasy_points_ppr: float