from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api import models, schemas
from src.api.database import get_db


router = APIRouter(prefix='/leagues', tags=['leagues'])

@router.post("/", response_model=schemas.LeagueOut)
def create_league(league: schemas.LeagueCreate, db: Session = Depends(get_db)):
    db_league = models.League(name=league.name)

    db.add(db_league)
    db.commit()
    db.refresh(db_league)
    
    return db_league

@router.post("/{league_id}", response_model = schemas.TeamOut)
def create_team(league_id: int, team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = models.Teams(name=team.name, league_id=league_id)

    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    return db_team

def name_to_id(name: str, db: Session = Depends(get_db)):
    x = name.replace("'", "").replace(";","")
    player = db.query(models.PlayerProjections).filter(models.PlayerProjections.name.like(f'%{x}%')).first()
    if not player:
        return
    return int(player.id)


@router.post("/{league_id}/{team_id}/ids")
def add_players_ids(league_id: int, team_id: int, body: schemas.PlayerIds, db: Session = Depends(get_db)):
    team = db.query(models.Teams).filter(models.Teams.id == team_id, models.Teams.league_id == league_id).first()

    players = db.query(models.PlayerProjections).filter(models.PlayerProjections.id.in_(body.player_ids)).all()

    team.players.extend(players)

    db.commit()

    return {"status": "success", "team_id": team_id, "players_added": len(players)}


@router.post("/{league_id}/{team_id}/names")
def add_players_names(league_id: int, team_id: int, body: schemas.PlayerNames, db: Session = Depends(get_db)):
    team = db.query(models.Teams).filter(models.Teams.id == team_id, models.Teams.league_id == league_id).first()

    ids = [name_to_id(name, db) for name in body.player_names]

    players = db.query(models.PlayerProjections).filter(models.PlayerProjections.id.in_(ids)).all()

    team.players.extend(players)

    db.commit()

    return {"status": "success", "team_id": team_id, "players_added": len(players)}