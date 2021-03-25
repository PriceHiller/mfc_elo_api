from typing import Optional

from pydantic import BaseModel

from API.Schemas import BaseInDB


class BasePlayer(BaseModel):
    player_name: str
    playfab_id: str
    discord_id: Optional[int]
    team_id: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "player_name": "Example",
                "playfab_id": "abcd1234"
            }
        }


class Player(BasePlayer):
    ...


class BasePlayerInDB(BasePlayer, BaseInDB):
    id: str


class PlayerInDB(BasePlayerInDB):
    ...
