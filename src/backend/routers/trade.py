from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.models import models, schemas
from src.database.database import get_db
from itertools import product
from copy import deepcopy
from src.authentication.auth import get_current_user

lineup_rules = {"QB": 1, "WR": 2, "RB": 2, "FLEX": 1, "TE": 1, "K": 1, "DST": 1}
trade_positions = ["QB", "WR1", "WR2", "RB1", "RB2", "FLEX", "TE"]


router = APIRouter(prefix='/trades', tags=['trades'])

# teams are always of the structure {"position": [("player_name", player_projection)]} list of tuples
# lineups are of form {"trade position": [("player_name, player_projection")]}


def sort_tuples(list_of_tuples):
    return sorted(list_of_tuples, key=lambda x: x[1], reverse=True)

def sum_points(list_of_tuples):
    total = 0
    for tuple in list_of_tuples:
        total += tuple[1]
    return total


def optimise_lineup(team: dict, lineup_rules: dict):
    lineup = {}
    backups = {}
    total_points = 0

    qbs = sort_tuples(team["QB"])
    lineup["QB"] = qbs[0] if qbs else None
    backups["QB"] = qbs[1][1] if len(qbs) > 1 else 0
    total_points += lineup["QB"][1] if lineup["QB"] else 0

    tes = sort_tuples(team["TE"])
    lineup["TE"] = tes[0] if tes else None
    backups["TE"] = tes[1][1] if len(tes) > 1 else 0
    total_points += lineup["TE"][1] if lineup["TE"] else 0

    ks = sort_tuples(team["K"])
    lineup["K"] = ks[0] if ks else None
    backups["K"] = ks[1][1] if len(ks) > 1 else 0
    total_points += lineup["K"][1] if lineup["K"] else 0

    dsts = sort_tuples(team["DST"])
    lineup["DST"] = dsts[0] if dsts else None
    backups["DST"] = dsts[1][1] if len(dsts) > 1 else 0
    total_points += lineup["DST"][1] if lineup["DST"] else 0

    wrs = sort_tuples(team["WR"])
    lineup["WR1"] = wrs[0] if len(wrs) > 0 else None
    lineup["WR2"] = wrs[1] if len(wrs) > 1 else None
    total_points += (lineup["WR1"][1] if lineup["WR1"] else 0)
    total_points += (lineup["WR2"][1] if lineup["WR2"] else 0)

    rbs = sort_tuples(team["RB"])
    lineup["RB1"] = rbs[0] if len(rbs) > 0 else None
    lineup["RB2"] = rbs[1] if len(rbs) > 1 else None
    total_points += (lineup["RB1"][1] if lineup["RB1"] else 0)
    total_points += (lineup["RB2"][1] if lineup["RB2"] else 0)

    remaining_wr = wrs[2:] if len(wrs) > 2 else []
    remaining_rb = rbs[2:] if len(rbs) > 2 else []
    flex_candidates = remaining_wr + remaining_rb
    flex_candidates = sort_tuples(flex_candidates)

    lineup["FLEX"] = flex_candidates[0] if flex_candidates else None
    total_points += lineup["FLEX"][1] if lineup["FLEX"] else 0

    if flex_candidates[0] in team["WR"]:
        backups["WR"] = wrs[3][1] if len(wrs) > 3 else 0
        backups["RB"] = rbs[2][1] if len(rbs) > 2 else 0
    else:
        backups["WR"] = wrs[2][1] if len(wrs) > 2 else 0
        backups["RB"] = rbs[3][1] if len(rbs) > 3 else 0

    backups["FLEX"] = (
        flex_candidates[1][1] if len(flex_candidates) > 1 else 0
    )

    lineup["POINTS"] = total_points

    return lineup, backups



def identify_positional_leverage(lineupA, lineupB):
    A_lev, B_lev = [], []
    for pos in ["QB", "WR1", "WR2", "RB1", "RB2", "FLEX", "TE"]:
        if not lineupA[pos] or not lineupB[pos]:
            continue
        if lineupA[pos][1] > lineupB[pos][1]:
            A_lev.append(pos)
        elif lineupB[pos][1] > lineupA[pos][1]:
            B_lev.append(pos)
    return list(product(A_lev, B_lev))


def trade(lineup1, team1, lineup2, team2, positions):
    copy_a = deepcopy(team1)
    copy_b = deepcopy(team2)
    proj_a = lineup1["POINTS"]
    proj_b = lineup2["POINTS"]

    for pos in positions:
        player_name_a = lineup1[pos][0]
        for copypos in copy_a:
            for i in range(len(copy_a[copypos])):
                if copy_a[copypos][i][0] == player_name_a:
                    a_pos = copypos
                    a_idx = i
                    break
        a_to_b = copy_a[a_pos].pop(a_idx)

        player_name_b = lineup2[pos][0]
        for copypos in copy_b:
            for j in range(len(copy_b[copypos])):
                if copy_b[copypos][j][0] == player_name_b:
                    b_pos = copypos
                    b_idx = j
                    break
        b_to_a = copy_b[b_pos].pop(b_idx)

        copy_a[a_pos].append(b_to_a)
        copy_b[b_pos].append(a_to_b)

    opt_a, repa = optimise_lineup(copy_a, lineup_rules)
    opt_b, repb = optimise_lineup(copy_b, lineup_rules)
    new_proj_a = opt_a["POINTS"]
    new_proj_b = opt_b["POINTS"]
    
    return new_proj_a - proj_a, new_proj_b - proj_b
    

def trades_evaluator(team1, team2):
    lineupA, replaceA = optimise_lineup(team1, lineup_rules)
    lineupB, replaceB = optimise_lineup(team2, lineup_rules)

    trades = identify_positional_leverage(lineupA, lineupB)

    good_trades = []

    for offer in trades:
        a_change, b_change = trade(lineupA, team1, lineupB, team2, offer)
        if a_change > 0 and b_change > 0:
            string = f"Trading {lineupA[offer[0]][0]} and {lineupA[offer[1]][0]} for {lineupB[offer[0]][0]} and {lineupB[offer[1]][0]} results in you gaining {a_change} points and them gaining {b_change} points."
            good_trades.append(string)
    
    return good_trades


def generate_team_dict(team):
    players = team.players
    player_dict = {}
    positions = ["QB", "WR", "RB", "TE", "K", "DST"]
    for pos in positions:
        player_dict[pos] = []
    
    for player in players:
        player_dict[player.position].append((player.name, player.fantasy_points_ppr))
    
    return player_dict


@router.get("/{league_id}/{team_id}", response_model=dict)
def identify_trades(league_id: int,
                    team_id: int,
                    db: Session = Depends(get_db),
                    current_user: models.Users = Depends(get_current_user)
                    ):
    your_team = db.query(models.Team).filter(models.Team.league_id == league_id,
                                             models.Team.id == team_id,
                                             models.Team.user_id == current_user.id).first()

    if not your_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No team with id {team_id} found")
    
    other_teams = db.query(models.Team).filter(models.Team.league_id == league_id,
                                               models.Team.id != team_id,
                                               models.Team.user_id == current_user.id).all()

    your_team_dict = generate_team_dict(your_team)

    optimum_team, replace_team = optimise_lineup(your_team_dict, lineup_rules)

    trades = {}
    for team in other_teams:
        player_dict = generate_team_dict(team)
        trades[team.name] = trades_evaluator(your_team_dict, player_dict)

    return {"optimal lineup": optimum_team, "trades": trades}



    








