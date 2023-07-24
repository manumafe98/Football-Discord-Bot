import requests
import discord

# Football api: https://www.football-data.org/documentation/quickstart
# Discord documentation: https://discordpy.readthedocs.io/en/latest/intro.html

top_5_ligues_array = [{"premier_league": 2021}, {"ligue_one": 2015}, {"bundesliga": 2002}, 
                      {"serie_a": 2019}, {"primeira_liga": 2017}]

endpoint_headers = {
    "X-Auth-Token": "aaf02ea4244745a5a8140e4f4cbdbc90"
}


for id in top_5_ligues_array:
    response = requests.get(f"https://api.football-data.org/v4/competitions/{list(id.values())[0]}/teams", 
                            headers=endpoint_headers)
    output = response.json()["teams"]
    for teams in output:
        print(teams["name"], teams["id"])