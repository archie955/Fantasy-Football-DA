from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


# User models

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserLogin(UserCreate):
    pass


# NFL player, team, and league models

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



# Token models for authentication

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]