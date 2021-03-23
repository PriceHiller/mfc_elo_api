from typing import Optional
from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import UUID4


class BasePlayer(BaseModel):
    player_name: str
    playfab_id: str

    class Config:
        schema_extra = {
            "example": {
                "player_name": "Example",
                "playfab_id": "abcd1234"
            }
        }


class Player(BasePlayer):
    steam64: Optional[int]


class PlayerID(Player):
    id: str
    team_id: Optional[str]
