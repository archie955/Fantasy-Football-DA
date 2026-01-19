Here team is a dictionary formatted as {"position": [("player_name", projection)]}
Trade positions is a dictionary containing the backup projection.
def optimise_lineup(team: dict, lineup_rules: dict):
    lineup = {}
    replace = {}
    lineup["POINTS"] = 0
    for position in lineup_rules:
        if position != "FLEX":
            sorted_list = sort_tuples(team[position])
            if position == "WR" or position == "RB":
                lineup[position+"1"] = sorted_list[0]
                lineup[position+"2"] = sorted_list[1]
                lineup["POINTS"] += sorted_list[0][1]
                lineup["POINTS"] += sorted_list[1][1]
            else:
                lineup[position] = sorted_list[:lineup_rules[position]]
                lineup["POINTS"] += sum_points(lineup[position])
                if len(sorted_list) > lineup_rules[position]:
                    replace[position] = sorted_list[lineup_rules[position]][1]
                else:
                    replace[position] = 0
        else:
            sorted_list_wr = sort_tuples(team["WR"])
            sorted_list_rb = sort_tuples(team["RB"])
            wr, rb = sorted_list_wr[2], sorted_list_rb[2]
            if wr[1] >= rb[1]:
                lineup["FLEX"] = [wr]
                lineup["POINTS"] += wr[1]
                if sorted_list_wr[3]:
                    replace["WR"] = sorted_list_wr[3][1]
                    replace["FLEX"] = max(sorted_list_wr[3][1], rb[1])
                else:
                    replace["WR"] = 0
                replace["RB"] = rb[1]
            else:
                lineup["FLEX"] = [rb]
                lineup["POINTS"] += rb[1]
                if len(sorted_list_rb) > 3 and len(sorted_list_rb[3]) > 1:
                    replace["RB"] = sorted_list_rb[3][1]
                    replace["FLEX"] = max(sorted_list_rb[3][1], wr[1])
                else:
                    replace["RB"] = 0
                replace["WR"] = wr[1]
    return lineup, replace


def identify_positional_leverage(lineupA, lineupB):
    A_lev = []
    B_lev = []

    for pos in trade_positions:
        if len(lineupB[pos]) > 1 and len(lineupA[pos]) <= 1:
            B_lev.append(pos)
        elif len(lineupB[pos]) <= 1 and len(lineupA[pos]) > 1:
            A_lev.append(pos)
        elif len(lineupB[pos]) <= 1 and len(lineupA[pos]) <= 1:
            return []
        elif lineupA[pos][1] > lineupB[pos][1]:
            A_lev.append(pos)
        else:
            B_lev.append(pos)
    return list(product(A_lev, B_lev))