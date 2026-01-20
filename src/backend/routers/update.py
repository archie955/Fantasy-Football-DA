from fastapi import Depends, APIRouter, status, HTTPException

from ...models import models
from ...database.database import get_db
from ...models import schemas
from sqlalchemy.orm import Session
from typing import List
from .get import get_teams
from src.authentication.auth import get_current_user

router = APIRouter(prefix="/update", tags=["Data"])

@router.put("/{league_id}/{team_id}")
def update_team(league_id: int,
                team_id: int,
                players_out: schemas.PlayerNames,
                players_in: schemas.PlayerNames,
                db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)
                ):
    team = db.query(models.Team).filter(models.Team.id == team_id, models.Team.league_id == league_id, models.Team.user_id == current_user).first()
    
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This team does not exist")
    
    p_out = []
    p_in = []

    for p in players_out:
        player = db.query(models.PlayerProjections).filter(models.PlayerProjections.name == p).first()
        if not player:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No player with name {p} exists")
        
        if player not in team.players:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Player {p} does not belong to this team")
        p_out.append(player)
    
    teams = get_teams(league_id, db)

    for p in players_in:
        player = db.query(models.PlayerProjections).filter(models.PlayerProjections.name == p).first()
        if not player:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No player with name {p} exists")
        
        for t in teams:
            if player in t.players:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Player {p} is not a free agent")
        p_in.append(player)

    for p in p_out:
        team.players.remove(p)

    for p in p_in:
        team.players.extend(p)

    db.commit()

    return {"status": "success", "team_id": team_id, "players removed": players_out, "players added": players_in, "new team": team.players}



@router.put("/{league_id}")
def team_trades(league_id: int,
                team1_id: int,
                team2_id: int,
                team1_players: List[schemas.PlayerNames],
                team2_players: List[schemas.PlayerNames],
                db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)
                ):
    team1 = db.query(models.Team).filter(models.Team.id == team1_id, models.Team.league_id == league_id, models.Team.user_id == current_user).first()

    if not team1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"One of the provided teams does not exist")
    
    team2 = db.query(models.Team).filter(models.Team.id == team2_id, models.Team.league_id == league_id, models.Team.user_id == current_user).first()

    if not team2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"One of the provided teams does not exist")

    p1 = []
    p2 = []

    for p in team1_players:
        player = db.query(models.PlayerProjections).filter(models.PlayerProjections.name == p).first()
        if not player:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No player with name {p} exists")
        
        if player not in team1.players:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Player {p} does not belong to this team")
        p1.append(player)

    for p in team2_players:
        player = db.query(models.PlayerProjections).filter(models.PlayerProjections.name == p).first()
        if not player:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No player with name {p} exists")
        
        if player not in team2.players:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Player {p} does not belong to this team")
        p2.append(player)

    for p in p1:
        team1.players.remove(p)
        team2.player.extend(p)

    for p in p2:
        team1.players.extend(p)
        team2.players.remove(p)

    db.commit()
    return {"status": "success", "team1_id": team1_id, "team2_id": team2_id, "team 1 players": team1_players, "team 2 players": team2_players}