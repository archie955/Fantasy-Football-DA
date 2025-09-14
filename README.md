This is a project where I will create a tool that will analyse NFL data to identify players that, within a given league, are worth picking up in NFL fantasy given the rules and teams. It will also possibly suggest trades of mutual upside, therefore trades that are likely to be accepted. 

The key structure will be:
1. Start with input data from the NFL for performance over the season and pre-season predictions of expected points in fantasy
2. Take the input data from the particular fantasy league.
3. Identify players that are over/under performing with expectations based on strength of schedule
4. Identify mutually beneficial trades that can be leveraged
5. Make recommendations of free agents that could be picked up and who they should be in place of

TO DO LIST:
- Add improved name to ids function to make adding players easier by using LIKE statement, so that as long as some of the name is added it works quickly
- Add function to optimise lineup
- Add function to mock trade with either 1 for 1 or 2 for 2 trades
- Add function that, for any given 2 teams, will rank their positions and determine if one team has leverage over the other for a trade. If and only if two or more positions is this true for will it return a positive result along with the positions and players names
- Add function that ties this all together, appending to a list all of the possible trades and how much of an improvement they are for both teams and the teams involved, most likely through a dictionary (list of dicts)
- Finally add the endpoint for this and allow it to simulate trades and find the optimal
- Then perhaps add visualisations of all the possible trades, this can be left though as visualisations are not that natural of an extension for a project like this.