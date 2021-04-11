from typing import List
from typing import Union
from typing import Optional

from pydantic import UUID4
from pydantic import Field

from API.Schemas import BaseInDB
from API.Schemas import BaseSchema
from API.Schemas.Mordhau.player import PlayerInDB


class BaseTeam(BaseSchema):
    team_name: str


class Team(BaseTeam):
    elo: int
    discord_id: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "team_name": "Example Team",
                "discord_id": 123456789,
                "elo": 1500
            }
        }


class CreateTeam(Team):
    ...


class BaseTeamInDB(Team, BaseInDB):
    ...


class TeamInDB(BaseTeamInDB):
    players: List[PlayerInDB]
