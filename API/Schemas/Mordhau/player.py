from typing import Optional
from typing import Any

from pydantic import BaseModel
from pydantic import Field


class BasePlayer(BaseModel):
    player_name: str
    playfab_id: str


class SteamPlayer(BasePlayer):
    steam64 = Field(min_length=17,
                    max_length=17)
