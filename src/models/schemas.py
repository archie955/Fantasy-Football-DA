from pydantic import BaseModel
from typing import List


class Projection(BaseModel):
    name: str
    team: str
    position: str
    fantasy_points_ppr: float


class LeagueCreate(BaseModel):
    name: str

class LeagueOut(LeagueCreate):
    id: int
    class Config:
        from_attributes = True

class TeamCreate(BaseModel):
    name: str

class TeamOut(TeamCreate):
    id: int
    league_id: int
    class Config:
        from_attributes = True

class PlayerOut(Projection):
    id: int
    class Config:
        from_attributes = True

class PlayerIds(BaseModel):
    player_ids: List[int]

class PlayerNames(BaseModel):
    player_names: List[str]