from pydantic import BaseModel

from API.Schemas import BaseInDB


class BaseTeam(BaseModel):
    team_name: str


class Team(BaseTeam):
    elo: int


class BaseTeamInDB(Team, BaseInDB):
    ...