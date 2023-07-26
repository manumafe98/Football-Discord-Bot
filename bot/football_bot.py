import discord
import requests
from datetime import date, timedelta
#from db.client import db_client

# Discord documentation: https://discordpy.readthedocs.io/en/stable/
# Message look like a table :https://stackoverflow.com/questions/63565825/how-to-make-data-to-be-shown-in-tabular-form-in-discord-py

CURRENT_DATE = date.today()


endpoint_headers = {
    "X-Auth-Token": "aaf02ea4244745a5a8140e4f4cbdbc90"
}

endpoint_params = {
    "lmit": 1,
    "dateFrom": str(CURRENT_DATE),
    "dateTo": str(CURRENT_DATE + timedelta(days=30))

}

team_id = input("enter team id: ")
response = requests.get(f"https://api.football-data.org/v4/teams/{team_id}/matches/", 
headers=endpoint_headers, params=endpoint_params)
output = response.json()

home_team_logo = output["matches"][0]["homeTeam"]["crest"]
home_team_name = output["matches"][0]["homeTeam"]["name"]

away_team_logo = output["matches"][0]["awayTeam"]["crest"]
away_team_name = output["matches"][0]["awayTeam"]["name"]

print(home_team_name, away_team_name)