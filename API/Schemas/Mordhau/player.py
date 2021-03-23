from typing import Optional

from pydantic import BaseModel


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
