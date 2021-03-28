from typing import List

from pydantic import BaseModel

from API.Schemas import BaseInDB
from API.Schemas.Mordhau.player import PlayerInDB


class BaseTeam(BaseModel):
    team_name: str


class Team(BaseTeam):
    elo: int


class CreateTeam(Team):
    ...


class BaseTeamInDB(Team, BaseInDB):
    ...


class TeamInDB(BaseTeamInDB):
    players: List[PlayerInDB]


class StrippedTeamInDB(BaseTeamInDB):
    ...

