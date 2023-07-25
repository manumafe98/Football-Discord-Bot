import requests
from db.client import db_client
from db.models.model import TopLeagueTeams

# Football api: https://www.football-data.org/documentation/quickstart

top_5_ligues_array = [{"premier_league": 2021}, {"ligue_one": 2015}, {"bundesliga": 2002}, 
                      {"serie_a": 2019}, {"primeira_liga": 2017}]

endpoint_headers = {
    "X-Auth-Token": "aaf02ea4244745a5a8140e4f4cbdbc90"
}


for league in top_5_ligues_array:
    response = requests.get(f"https://api.football-data.org/v4/competitions/{list(league.values())[0]}/teams", 
                            headers=endpoint_headers)
    teams = response.json()["teams"]
    for team in teams:
        new_team = TopLeagueTeams(team_name = team["name"],
                                  team_id = team["id"],
                                  league_name = list(league.keys())[0],
                                  league_id = list(league.values())[0])
        data = new_team.model_dump()
        db_client.league_teams.insert_one(data)
