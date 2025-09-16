from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.api import models, schemas
from src.api.database import get_db
from typing import List
from collections import OrderedDict
from itertools import product
from copy import deepcopy

# I intend to format each team as a dictionary so i can easily extract a particular players projection. The exact form will be {"name": projection}
# I will have a dictionary for the team of interest (that I am hoping to find trades for) then the other teams will be a dict of dicts {"team_name": {"player_name": projection}}

lineup_rules = {"QB": 1, "WR": 2, "RB": 2, "FLEX": 1, "TE": 1, "K": 1, "DST": 1}
trade_positions = ["QB", "WR1", "WR2", "RB1", "RB2", "FLEX", "TE"]


router = APIRouter(prefix='/trades', tags=['trades'])

   

def sort_tuples(list_of_tuples):
    return sorted(list_of_tuples, key=lambda x: x[1])

def sum_points(list_of_tuples):
    total = 0
    for tuple in list_of_tuples:
        total += tuple[1]
    return total

# Here team is a dictionary formatted as {"position": [("player_name", projection)]}
# Trade positions is a dictionary containing the backup projection.
# def optimise_lineup(team: dict, lineup_rules: dict):
#     lineup = {}
#     replace = {}
#     lineup["POINTS"] = 0
#     for position in lineup_rules:
#         if position != "FLEX":
#             sorted_list = sort_tuples(team[position])
#             if position == "WR" or position == "RB":
#                 lineup[position+"1"] = sorted_list[0]
#                 lineup[position+"2"] = sorted_list[1]
#                 lineup["POINTS"] += sorted_list[0][1]
#                 lineup["POINTS"] += sorted_list[1][1]
#             else:
#                 lineup[position] = sorted_list[:lineup_rules[position]]
#                 lineup["POINTS"] += sum_points(lineup[position])
#                 if len(sorted_list) > lineup_rules[position]:
#                     replace[position] = sorted_list[lineup_rules[position]][1]
#                 else:
#                     replace[position] = 0
#         else:
#             sorted_list_wr = sort_tuples(team["WR"])
#             sorted_list_rb = sort_tuples(team["RB"])
#             wr, rb = sorted_list_wr[2], sorted_list_rb[2]
#             if wr[1] >= rb[1]:
#                 lineup["FLEX"] = [wr]
#                 lineup["POINTS"] += wr[1]
#                 if sorted_list_wr[3]:
#                     replace["WR"] = sorted_list_wr[3][1]
#                     replace["FLEX"] = max(sorted_list_wr[3][1], rb[1])
#                 else:
#                     replace["WR"] = 0
#                 replace["RB"] = rb[1]
#             else:
#                 lineup["FLEX"] = [rb]
#                 lineup["POINTS"] += rb[1]
#                 if len(sorted_list_rb) > 3 and len(sorted_list_rb[3]) > 1:
#                     replace["RB"] = sorted_list_rb[3][1]
#                     replace["FLEX"] = max(sorted_list_rb[3][1], wr[1])
#                 else:
#                     replace["RB"] = 0
#                 replace["WR"] = wr[1]
#     return lineup, replace

def optimise_lineup(team: dict, lineup_rules: dict):
    """
    Given a team (dict of position -> list of (player_name, proj)),
    choose the optimal starting lineup and identify the best backups
    for points-over-replacement (trade evaluation).
    """
    lineup = {}
    backups = {}
    total_points = 0

    # --- Quarterback ---
    qbs = sort_tuples(team["QB"])
    lineup["QB"] = qbs[0] if qbs else None
    backups["QB"] = qbs[1][1] if len(qbs) > 1 else 0
    total_points += lineup["QB"][1] if lineup["QB"] else 0

    # --- Tight End ---
    tes = sort_tuples(team["TE"])
    lineup["TE"] = tes[0] if tes else None
    backups["TE"] = tes[1][1] if len(tes) > 1 else 0
    total_points += lineup["TE"][1] if lineup["TE"] else 0

    # --- Kicker ---
    ks = sort_tuples(team["K"])
    lineup["K"] = ks[0] if ks else None
    backups["K"] = ks[1][1] if len(ks) > 1 else 0
    total_points += lineup["K"][1] if lineup["K"] else 0

    # --- Defense ---
    dsts = sort_tuples(team["DST"])
    lineup["DST"] = dsts[0] if dsts else None
    backups["DST"] = dsts[1][1] if len(dsts) > 1 else 0
    total_points += lineup["DST"][1] if lineup["DST"] else 0

    # --- Wide Receivers ---
    wrs = sort_tuples(team["WR"])
    lineup["WR1"] = wrs[0] if len(wrs) > 0 else None
    lineup["WR2"] = wrs[1] if len(wrs) > 1 else None
    backups["WR"] = wrs[2][1] if len(wrs) > 2 else 0
    total_points += (lineup["WR1"][1] if lineup["WR1"] else 0)
    total_points += (lineup["WR2"][1] if lineup["WR2"] else 0)

    # --- Running Backs ---
    rbs = sort_tuples(team["RB"])
    lineup["RB1"] = rbs[0] if len(rbs) > 0 else None
    lineup["RB2"] = rbs[1] if len(rbs) > 1 else None
    backups["RB"] = rbs[2][1] if len(rbs) > 2 else 0
    total_points += (lineup["RB1"][1] if lineup["RB1"] else 0)
    total_points += (lineup["RB2"][1] if lineup["RB2"] else 0)

    # --- FLEX (best remaining WR or RB not already used) ---
    remaining_wr = wrs[2:] if len(wrs) > 2 else []
    remaining_rb = rbs[2:] if len(rbs) > 2 else []
    flex_candidates = remaining_wr + remaining_rb
    flex_candidates = sort_tuples(flex_candidates)

    lineup["FLEX"] = flex_candidates[0] if flex_candidates else None
    total_points += lineup["FLEX"][1] if lineup["FLEX"] else 0

    # Best backup at FLEX = best of next WR/RB after FLEX choice
    backups["FLEX"] = (
        flex_candidates[1][1] if len(flex_candidates) > 1 else 0
    )

    # Save total
    lineup["POINTS"] = total_points

    return lineup, backups



# def identify_positional_leverage(lineupA, lineupB):
#     A_lev = []
#     B_lev = []
# 
#     for pos in trade_positions:
#         if len(lineupB[pos]) > 1 and len(lineupA[pos]) <= 1:
#             B_lev.append(pos)
#         elif len(lineupB[pos]) <= 1 and len(lineupA[pos]) > 1:
#             A_lev.append(pos)
#         elif len(lineupB[pos]) <= 1 and len(lineupA[pos]) <= 1:
#             return []
#         elif lineupA[pos][1] > lineupB[pos][1]:
#             A_lev.append(pos)
#         else:
#             B_lev.append(pos)
#     return list(product(A_lev, B_lev))

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



# Add function that completes the trade using deepcopies then reoptimises the lineup, then returns the trade details if it works, otherwise doesn't. Can do this by 
# returning a boolean with it that I only append if true or something like this.
# Trade identifier can then function by checking every single trade within the group and return a list of the trades
# After this I can make the master function and actual router than will apply trade_identifier to all teams with your specified team. This will then return a dict of lists 
# or something I haven't settled on the return types, but will return the information.

def trade(lineup1, backups1, lineup2, backups2, positions):
    new_a = deepcopy(lineup1)
    new_b = deepcopy(lineup2)
    proj_a = 0
    proj_b = 0
    new_proj_a = 0
    new_proj_b = 0

    for pos in positions:
        proj_a += new_a[pos][1]
        proj_b += new_b[pos][1]
        new_a[pos], new_b[pos] = new_b[pos], new_a[pos]
        new_proj_a += max(new_a[pos][1], backups1[pos.replace("1","").replace("2","")])
        new_proj_b += max(new_b[pos][1], backups2[pos.replace("1","").replace("2","")])
    
    return new_proj_a - proj_a, new_proj_b - proj_b
    



def trades_evaluator(team1, team2):
    lineupA, replaceA = optimise_lineup(team1, lineup_rules)
    lineupB, replaceB = optimise_lineup(team2, lineup_rules)

    trades = identify_positional_leverage(lineupA, lineupB)

    good_trades = []

    for offer in trades:
        a_change, b_change = trade(lineupA, replaceA, lineupB, replaceB, offer)
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
def identify_trades(league_id: int, team_id: int, db: Session = Depends(get_db)):
    your_team = db.query(models.Teams).filter(models.Teams.league_id == league_id, models.Teams.id == team_id).first()

    if not your_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No team with id {team_id} found")
    
    other_teams = db.query(models.Teams).filter(models.Teams.league_id == league_id, models.Teams.id != team_id).all()

    your_team_dict = generate_team_dict(your_team)
    trades = {}
    teams = {}
    for team in other_teams:
        player_dict = generate_team_dict(team)
        trades[team.name] = trades_evaluator(your_team_dict, player_dict)

    return trades



    








