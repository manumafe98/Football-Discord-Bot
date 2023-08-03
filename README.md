## Football Discord Bot

This is a bot that you can add to your discord server to check the next match of one of the teams of the top 5 leagues.

It uses the [Football Coverage API](https://www.football-data.org/coverage) to obtain the information and the discord.py library for the logic.

## Usage

When you invite the bot to the channel you have 3 available commands.
- `$instructions`: That gives you a brief explanation on how to use the main commands.
- `$list_teams`: Expects one of the top leagues as a parameter in lower case and snake case, and outputs all the teams of that league with their respectives `IDs` that you need for the usage of the next command.
- `$next_match`: Expects a team id as a parameter and outputs the next match of that team.

![bot_test_image](https://github.com/manumafe98/Football-Discord-Bot/assets/95315128/bd3b4ebb-d47e-4395-ba6e-1718e78ccdcd)