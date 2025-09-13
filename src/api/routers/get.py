from fastapi import status, Depends, APIRouter, HTTPException
from ..database import get_db
from ..config import settings
from .. import models, schemas
from sqlalchemy.orm import Session
from decimal import Decimal
from typing import List
import requests
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
    





@router.get("/", response_model=dict)
def fetchData(db: Session = Depends(get_db)):
    playerdataURL = f"https://baker-api.sportsdata.io/baker/v2/nfl/projections/players/full-season/2025REG/avg?key={settings.API_KEY}"
    playerDataResponse = requests.get(playerdataURL)
    playerData = playerDataResponse.json()
    filtered_data = [
        {
            "player_id": player["PlayerID"],
            "name": player["Name"],
            "team": player["Team"],
            "position": player["Position"],
            "passing_yards": player["passing_yards"],
            "passing_touchdowns": player["passing_touchdowns"],
            "rushing_yards": player["rushing_yards"],
            "rushing_touchdowns": player["rushing_touchdowns"],
            "fumbles_lost": player["fumbles_lost"],
            "catches": player["catches"],
            "receiving_yards": player["receiving_yards"],
            "receiving_touchdowns": player["receiving_touchdowns"],
            "fantasy_points_ppr": player["fantasy_points_ppr"]
        }
        for player in playerData
    ]
    for item in filtered_data:
        db_item = models.Players(**item)
        db.add(db_item)
    
    db.commit()
    return {"status":"Success", "Inserted": len(filtered_data)}