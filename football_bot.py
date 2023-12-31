import os
import requests
import discord
from discord.ext import commands
from discord.utils import find
from datetime import date, timedelta, datetime
from table2ascii import table2ascii as t2a, PresetStyle


CURRENT_DATE = date.today()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

top_5_ligues_array = [{"premier_league": 2021}, {"ligue_one": 2015}, {"bundesliga": 2002}, 
                      {"serie_a": 2019}, {"primeira_liga": 2017}]

endpoint_headers = {
    "X-Auth-Token": os.environ.get("API_KEY")
}

endpoint_params = {
    "lmit": 1,
    "dateFrom": str(CURRENT_DATE),
    "dateTo": str(CURRENT_DATE + timedelta(days=30))

}


# Handles errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Oops!", 
                              description="The command you inputed has missing arguments. " \
                              "Please check `$instructions` for more information", 
                              colour=discord.Colour(0x4a90e2))
        
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Sorry!", 
                              description="This command does not exist. " \
                              "Please check `$instructions` for more information", 
                              colour=discord.Colour(0x4a90e2))
        
        await ctx.send(embed=embed)


# Send a greetings message and how to start using it
@bot.event
async def on_guild_join(guild):
    general = discord.utils.get(guild.text_channels, name="general")
    if general and general.permissions_for(guild.me).send_messages:
        embed = discord.Embed(title="Hello!", 
                              description="To start using my features, use `$instructions`", 
                              colour=discord.Colour(0x4a90e2))
        await general.send(embed=embed)
    else:
        available_text_channels = [channel for channel in guild.text_channels 
                                   if channel.permissions_for(guild.me).send_messages]
        if available_text_channels:
            first_available_channel = available_text_channels[0]
            embed = discord.Embed(title="Hello!", 
                                  description="To start using my features, use `$instructions`", 
                                  colour=discord.Colour(0x4a90e2))
            await first_available_channel.send(embed=embed)


# Minimal how to use the bot message
@bot.command(name="instructions")
async def help(ctx):
    embed = discord.Embed(title="Instructions", 
                          description="With this bot you can get the next match of your favourite team!." \
                          "\nAll the commands are in lower case and snake case", 
                          colour=discord.Colour(0x4a90e2))

    embed.add_field(name="$list_teams", 
                    value="This command expects one of the top 5 leagues as parameters of the command," \
                    "and as output gives you a list of all the teams of that league with their respective ids." \
                    "\n**Example**: ```$list_teams premier_league```")
    embed.add_field(name="$next_match", 
                    value="With the previously gotten id you can get the next match of that team." \
                    "\n**Example**: ```$next_match 61```")

    await ctx.send(embed=embed)


# Get top 5 leagues teams with id, league name and league id
@bot.command(name="list_teams")
async def list_teams(ctx, inputed_league):
    body_array = []

    for league in top_5_ligues_array:
        if list(league.keys())[0] == inputed_league:
            response = requests.get(f"https://api.football-data.org/v4/competitions/{list(league.values())[0]}/teams", 
                                    headers=endpoint_headers)
            teams = response.json()["teams"]
            for team in teams:
                body_array.append([team["name"], team["id"]])

    table = t2a(
        header=["Team", "Team Id"],
        body=body_array,
        style=PresetStyle.thin_compact
    )

    await ctx.send(f"```\n{table}\n```")


# Get Team next match
@bot.command(name="next_match")
async def list_teams(ctx, team_id):
    response = requests.get(f"https://api.football-data.org/v4/teams/{team_id}/matches/", 
    headers=endpoint_headers, params=endpoint_params)
    output = response.json()

    home_team_logo = output["matches"][0]["homeTeam"]["crest"]
    home_team_name = output["matches"][0]["homeTeam"]["name"]

    away_team_logo = output["matches"][0]["awayTeam"]["crest"]
    away_team_name = output["matches"][0]["awayTeam"]["name"]


    timestamp = output["matches"][0]["utcDate"]
    datetime_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    formatted_date = datetime_obj.strftime("%d/%m")
    
    datetime_now = datetime.utcnow()

    remaining_time_until_match = (datetime_obj - datetime_now)

    if "day" in str(remaining_time_until_match):
        days_str, time_str = str(remaining_time_until_match).split(",")
        remaining_days = days_str.split()[0]
        remaining_hours = time_str.split(":")[0]
        description_text = f"Remaining time until the match, {remaining_days} days and {remaining_hours} hours"
    elif timedelta(hours=1) > remaining_time_until_match:
        description_text = f"Less than 1 hour remaining for the match"
    else:
        remaining_hours = str(remaining_time_until_match).split(":")[0]
        description_text = f"Remaining time until the match, {remaining_hours} hours"

    
    r = requests.get(f"https://api.football-data.org/v4/teams/{team_id}", headers=endpoint_headers)
    team_name = r.json()["name"]

    embed = discord.Embed(title=f"{team_name} next match is on the day {formatted_date}",
                          description=description_text,
                          colour=discord.Colour(0x4a90e2), url="https://manumafe98.github.io/cv/")

    embed.add_field(name="Home Team", value=home_team_name, inline=True)
    embed.add_field(name="Away Team", value=away_team_name, inline=True)
    
    
    embed1 = discord.Embed(url="https://manumafe98.github.io/cv/")
    embed2 = discord.Embed(url="https://manumafe98.github.io/cv/")

    embed1.set_image(url=home_team_logo)
    embed2.set_image(url=away_team_logo)

    await ctx.send(embeds=[embed, embed1, embed2])


bot.run(os.environ.get("BOT_TOKEN"))
