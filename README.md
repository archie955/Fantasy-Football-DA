# NFL Fantasy Trade Analysis API
This is a backend API that identifies mutually beneficial fantasy NFL trades between teams in a league, using player performance projections and roster structures. It consists of a full API, SQL (PostgreSQL) database integration, as well as statistical reasoning for the trade identification.

## Tech Stack:
- Language: Python
- Framework: FastAPI (REST API)
- Database: PostgreSQL (integrated via SQLAlchemy for the ORM & Alembic for migrations)
- Data Models and Schemas: Pydantic
- Net Architecture: Backend-only (Not frontend or deployment, HTTP request only)

## How it works:
Once a league, teams, and player rosters are created in the database, the API can run a trade analysis function that identifies trades offering statistical benefit to both teams involved.

I define a “Well-Founded” trade as one in which both participants increase their projected weekly starter points as a result of said trade.<br>
For instance, suppose the following setup:
- Team A: QBs (20, 18), TEs (8, 6) → total starter value: 28
- Team B: QBs (18, 15), TEs (12, 11) → total starter value: 30<br> 
#### If A and B swap their QB1 and TE1:
- Team A → (QBs 18,18; TEs 12,6) → 30 points
- Team B → (QBs 20,15; TEs 11,8) → 31 points<br> 
#### Both teams gain overall efficiency in what is an often overlooked trade due to conventional biases (e.g. positional value).

This tool focuses on identifying position groups where mutually beneficial exchanges may exist, leaving finer negotiation details to user judgment due to the lack of context surrounding the league (e.g. who is in it, what teams they follow, inside jokes and so on...)

## Algorithmic Approach:
The analysis uses a heuristic search over possible trade combinations:
- Considers only 2-for-2 trades between positions where each team has leverage. This is because any possible 1-for-1 or 1-for-2 trade will still be found by just appending two low scoring non-starters, which can easily be filtered out by the people in the trade, whilst trades involving more than this many players are increasingly rare and almost always context dependent, so for the sake of computational complexity are left out, hence:
- Skips exhaustive trade enumeration (which grows factorially with trade size).

## Limitations:
- Currently it is heuristic. A more exhuastive approach could be taken to check every single possible trade but this would be very slow.
- Ignores contextual factors such as injury risk (certain players being known for rarely finishing a season), as well as bye-weeks (this program considers rest of season projections so is not inaccurate, but it would promote a trade on the week a player isn't playing where, whilst the trade is still good, it should obviously be delayed a week)
- Currently supports only one scoring ruleset (point-per-reception) as well as one positional ruleset (standard flex with 2 wide receivers, 2 running backs and 1 flex of wide receiver or running back, as oppose to superflex etc)

## Data
The data has been gathered from <a href="https://www.fantasypros.com/nfl/rankings/qb.php">Fantasy Pros</a>
