from typing import Optional
from typing import Any

from pydantic import BaseModel
from pydantic import Field


class BaseTeam(BaseModel):
    team_name: str


class Team(BaseTeam):
    elo: int
