from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api import models, schemas
from src.api.database import get_db
from typing import List
from collections import OrderedDict
from itertools import product

# I intend to format each team as a dictionary so i can easily extract a particular players projection. The exact form will be {"name": projection}
# I will have a dictionary for the team of interest (that I am hoping to find trades for) then the other teams will be a dict of dicts {"team_name": {"player_name": projection}}

lineup_rules = OrderedDict([("QB", 1), ("WR", 2), ("RB", 2), ("FLEX", 1), ("TE", 1), ("K", 1), ("DST", 1)])
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
def optimise_lineup(team: dict, lineup_rules: dict):
    lineup = {}
    points_over_replacement = {}
    lineup["POINTS"] = 0
    for position, count in lineup_rules.items():
        if position != "FLEX":
            sorted_list = sort_tuples(team[position])
            if position == "WR" or position == "RB":
                lineup[position+"1"] = sorted_list[0]
                lineup[position+"2"] = sorted_list[1]
                lineup["POINTS"] += sorted_list[0][1]
                lineup["POINTS"] += sorted_list[1][1]
            else:
                lineup[position] = sorted_list[:count]
                lineup["POINTS"] += sum_points(lineup[position])
                if sorted_list[count]:
                    trade_positions[position] = sorted_list[count][1]
                else:
                    trade_positions[position] = 0
        else:
            sorted_list_wr = sort_tuples(team["WR"])
            sorted_list_rb = sort_tuples(team["RB"])
            wr, rb = sorted_list_wr[2], sorted_list_rb[2]
            if wr[1] >= rb[1]:
                lineup["FLEX"] = [wr]
                lineup["POINTS"] += wr[1]
                if sorted_list_wr[3]:
                    trade_positions["WR"] = sorted_list_wr[3][1]
                    trade_positions["FLEX"] = max(sorted_list_wr[3][1], rb[1])
                else:
                    trade_positions["WR"] = 0
                trade_positions["RB"] = rb[1]
            else:
                lineup["FLEX"] = [rb]
                lineup["POINTS"] += rb[1]
                if sorted_list_rb[3]:
                    trade_positions["RB"] = sorted_list_rb[3][1]
                    trade_positions["FLEX"] = max(sorted_list_rb[3][1], wr[1])
                else:
                    trade_positions["RB"] = 0
                trade_positions["WR"] = wr[1]
    return lineup, trade_positions


def identify_positional_leverage(lineupA, lineupB):
    A_lev = []
    B_lev = []

    for pos in trade_positions:
        if lineupA[pos][1] > lineupB[pos][1]:
            A_lev.append[pos]
        else:
            B_lev.append(pos)
    return list(product(A_lev, B_lev))


# Add function that completes the trade using deepcopies then reoptimises the lineup, then returns the trade details if it works, otherwise doesn't. Can do this by 
# returning a boolean with it that I only append if true or something like this.
# Trade identifier can then function by checking every single trade within the group and return a list of the trades
# After this I can make the master function and actual router than will apply trade_identifier to all teams with your specified team. This will then return a dict of lists 
# or something I haven't settled on the return types, but will return the information.

def trade_identifier(team1, team2):
    lineupA, replaceA = optimise_lineup(team1, lineup_rules)
    lineupB, replaceB = optimise_lineup(team1, lineup_rules)

    trades = identify_positional_leverage(lineupA, lineupB)

    








