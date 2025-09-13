from pydantic import BaseModel
from typing import Optional, List, Dict

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

class Projection(BaseModel):
    name: str
    team: str
    position: str
    fantasy_points_ppr: float

class Players(BaseModel):
    player_1: str
    player_2: str
    player_3: str
    player_4: str
    player_5: str
    player_6: str
    player_7: str
    player_8: str
    player_9: str
    player_10: str
    player_11: str
    player_12: str
    player_13: str
    player_14: str
    player_15: str
    player_16: Optional[str]
    player_17: Optional[str]
    player_18: Optional[str]

class Team(BaseModel):
    team_name: str
    players: Players

class League(BaseModel):
    league_name: str
    teams: Team

