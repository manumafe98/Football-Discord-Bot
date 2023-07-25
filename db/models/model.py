from pydantic import BaseModel


class TopLeagueTeams(BaseModel):
    team_name: str
    team_id: int
    league_name: str
    league_id: int
