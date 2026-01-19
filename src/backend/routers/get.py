from fastapi import Depends, APIRouter, status, HTTPException

from ...models import models
from ...database.database import get_db
from ...models import schemas
from sqlalchemy.orm import Session
from typing import List
import pandas as pd

router = APIRouter(prefix="/fetchdata", tags=["Data"])


@router.get("/csv", response_model=dict)
def csv_to_sql(db: Session = Depends(get_db)):

    files = {
        "QB": "data/FantasyPros_2025_Ros_QB_Rankings.csv",
        "RB": "data/FantasyPros_2025_Ros_RB_Rankings.csv",
        "WR": "data/FantasyPros_2025_Ros_WR_Rankings.csv",
        "DST": "data/FantasyPros_2025_Ros_DST_Rankings.csv",
        "K": "data/FantasyPros_2025_Ros_K_Rankings.csv",
        "TE": "data/FantasyPros_2025_Ros_TE_Rankings.csv",
    }

    inserted_count = 0

    for pos, filepath in files.items():
        df = pd.read_csv(filepath)

        df.columns = df.columns.str.strip().str.upper()

        data = df.to_dict(orient="records")

        filtered_data = [
            {
                "name": row.get("PLAYER NAME"),
                "team": row.get("TEAM"),
                "position": pos,
                "fantasy_points_ppr": row.get("PROJ. FPTS"),
            }
            for row in data
        ]

        for item in filtered_data:
            db_item = models.PlayerProjections(**item)
            db.add(db_item)

        inserted_count += len(filtered_data)

    db.commit()

    return {"status": "Success", "Inserted": inserted_count}


@router.get("/", response_model=List[schemas.LeagueOut])
def get_leagues(db: Session = Depends(get_db)):
    leagues = db.query(models.League).all()

    if not leagues:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No Leagues Found')

    return leagues


@router.get("/{league_id}", response_model=List[schemas.TeamOut])
def get_teams(league_id: int, db: Session = Depends(get_db)):
    teams = db.query(models.Teams).filter(models.Teams.league_id == league_id).all()

    if not teams:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Either no Teams belong to this league or the league doesn't exist")

    return teams


@router.get("/{league_id}/{team_id}", response_model=List[schemas.PlayerOut])
def get_players(league_id: int, team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.Teams).filter(models.Teams.id == team_id, models.Teams.league_id == league_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This team does not exist")
    return team.players