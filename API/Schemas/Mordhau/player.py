from typing import Optional
from typing import Any

from pydantic import BaseModel
from pydantic import Field


class BasePlayer(BaseModel):
    player_name: str
    playfab_id: str
    team_id: str


class Player(BasePlayer):
    steam64: Optional[str] = None
