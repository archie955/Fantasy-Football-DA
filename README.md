# NFL Fantasy Trade Analysis Tool

## Programme structure
This is all programmed using Python, with a SQL (Postgres) Database. The REST API is built with FastAPI, and the database is handled using Alembic migrations and SQLAlchemy with Pydantic as an ORM. The function is, once the league has been created, teams added, and players added per team in the database you can model run the trading function to identify statistically well-founded trades (elaborated on below).



## Well-Foundedness in a trade
A trade is considered statistically well-founded if it is of statistical benefit to both participants. In the case where this is not true, one of the teams reasoning for taking such as trade must be purely contextual and therefore not worth identifying using a tool, but rather whatever that context is. To give an example, consider the following situation. Suppose both team A and team B have 2 quarterbacks and 2 tight ends (QB and TE from here on out), and the rules are such that only 1 QB and 1 TE can start (no superflex). Team A's QBs have the projected weekly points of 20 and 18 (the better being labelled QB1, the bench player being QB2), and team A's TEs have a projection of 8 and 6 points, giving a projected combined starter value of 28 points per week. Team B, on the other hand, has their QBs with 18 and 15 points, TEs with 12 and 11 points, for a combined 30 starter points per week. In this scenario, if both teams traded their QB1 and TE1 to one another, team A ends up with QBs 18 and 18, TEs 12 and 6 for a total of 30 points per week. Team B now has QBs 20 and 15 with TEs 11 and 8, giving a total of 31 points per week. Both teams have had an increase in their expected points per week, but this is a trade that would often not be considered for the following reasons:
1. Quarterbacks are more valuable than tight ends, offering far more raw points. The thing is, raw points do not matter but rather points over replacement.
2. This is a trade involving a lot of starters, often avoided.

Team B here could try to shift the trade further in their favour by offering TE 2, increasing them to 32 points and decreasing team A to 29 points, still beneficial for both but better for team B, but likewise team A could demand TE 1. This will come down to the context of who is in the trade, who needs it more etc. This tool should not be taken as identifying every possible trade, but rather highlighting position groups where a mutually beneficial trade exists between two teams, the fine details can be tweaked freely.

## Limitations
The main limitation here is that this tool is heuristic, it does not consider every single trade possibility as this information space grows factorially with trade size. Instead, it considers 2 for 2 trades between positions where each team has leverage (so all pairs that can be formed from the cartesian product of team A's leverage over B with team B's leverage over A). Once again, this is not a tool to identify every single possible trade, but rather a particular class of easily missed trade.

## Data
The data has been gathered from https://www.fantasypros.com/nfl/rankings/qb.php