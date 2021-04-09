from typing import Optional
from typing import Union

from pydantic import Field
from pydantic import UUID4

from API.Schemas import BaseInDB
from API.Schemas import BaseSchema


class BasePlayer(BaseSchema):
    player_name: str
    playfab_id: str
    discord_id: Optional[int]

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
    ...


class PlayerInDB(BasePlayerInDB):
    team_id: Optional[Union[UUID4, str, int]] = Field(..., minlength=32, maxlength=36)
    ambassador: Optional[bool]
