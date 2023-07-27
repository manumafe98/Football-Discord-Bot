import discord
import requests
from datetime import date, timedelta
from pydantic import BaseModel
from table2ascii import table2ascii as t2a, PresetStyle


# Football api: https://www.football-data.org/documentation/quickstart
# Discord documentation: https://discordpy.readthedocs.io/en/stable/
# Message look like a table: https://stackoverflow.com/questions/63565825/how-to-make-data-to-be-shown-in-tabular-form-in-discord-py

CURRENT_DATE = date.today()


top_5_ligues_array = [{"premier_league": 2021}, {"ligue_one": 2015}, {"bundesliga": 2002}, 
                      {"serie_a": 2019}, {"primeira_liga": 2017}]

class TopLeagueTeams(BaseModel):
    team_name: str
    team_id: int
    league_name: str
    league_id: int


endpoint_headers = {
    "X-Auth-Token": "aaf02ea4244745a5a8140e4f4cbdbc90"
}

endpoint_params = {
    "lmit": 1,
    "dateFrom": str(CURRENT_DATE),
    "dateTo": str(CURRENT_DATE + timedelta(days=30))

}

# Get top 5 leagues teams with id, league name and league id
body_array = []

for league in top_5_ligues_array:
    response = requests.get(f"https://api.football-data.org/v4/competitions/{list(league.values())[0]}/teams", 
                            headers=endpoint_headers)
    teams = response.json()["teams"]
    for team in teams:
        body_array.append([team["name"], team["id"], list(league.keys())[0], list(league.values())[0]])

table = t2a(
    header=["Team", "Team Id", "League", "League Id"],
    body=body_array,
    style=PresetStyle.thin_compact
)

# Get Team next match
# team_id = input("enter team id: ")
# response = requests.get(f"https://api.football-data.org/v4/teams/{team_id}/matches/", 
# headers=endpoint_headers, params=endpoint_params)
# output = response.json()

# home_team_logo = output["matches"][0]["homeTeam"]["crest"]
# home_team_name = output["matches"][0]["homeTeam"]["name"]

# away_team_logo = output["matches"][0]["awayTeam"]["crest"]
# away_team_name = output["matches"][0]["awayTeam"]["name"]

# print(home_team_name, away_team_name)