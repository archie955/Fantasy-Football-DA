from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api import models, schemas
from src.api.database import get_db
from typing import List
from collections import OrderedDict

# I intend to format each team as a dictionary so i can easily extract a particular players projection. The exact form will be {"name": projection}
# I will have a dictionary for the team of interest (that I am hoping to find trades for) then the other teams will be a dict of dicts {"team_name": {"player_name": projection}}

lineup_rules = OrderedDict([("QB", 1), ("WR", 2), ("RB", 2), ("FLEX", 1), ("TE", 1), ("K", 1), ("DST", 1)])


router = APIRouter(prefix='/trades', tags=['trades'])

def identify_candidates()

# Here team is a dictionary formatted as {"position": [("player_name", projection)]}
def optimise_lineup(team: dict, lineup_rules: dict):
    lineup = {}
    for position, count in lineup_rules.items():
        if position != "FLEX":
            