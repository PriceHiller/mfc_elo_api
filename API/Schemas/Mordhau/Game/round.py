from typing import Union
from typing import List

from pydantic import Field
from pydantic import UUID4

from API.Schemas import BaseInDB
from API.Schemas import BaseSchema


class BaseRoundPlayer(BaseSchema):
    team_id: UUID4
    team_number: int


class RoundPlayer(BaseRoundPlayer):
    round_id: Union[UUID4, str, int] = Field(..., minlength=32, maxlength=36)
    player_id: Union[UUID4, str, int] = Field(..., minlength=32, maxlength=36)
    score: int
    kills: int
    deaths: int
    assists: int


class CreateRoundPlayer(RoundPlayer):
    ...

    class Config:
        schema_extra = {
            "example": {
                "round_id": "uuid",
                "player_id": "uuid",
                "team_id": "uuid",
                "team_number": 0,
                "score": 0,
                "kills": 0,
                "deaths": 0,
                "assists": 0
            }
        }


class BaseRoundPlayerInDB(RoundPlayer, BaseInDB):
    set_id: UUID4
    match_id: UUID4
    ...


class RoundPlayerInDB(BaseRoundPlayerInDB):
    ...


class CreateRoundPlayers(BaseSchema):
    class Config:
        schema_extra = {
            "example": {
                "round_players": [CreateRoundPlayer.Config.schema_extra["example"]]
            }
        }
    round_players: List[CreateRoundPlayer]


class BaseRound(BaseSchema):
    set_id: Union[UUID4, str, int] = Field(..., minlength=32, maxlength=36)


class Round(BaseRound):
    class Config:
        schema_extra = {
            "example": {
                "set_id": "uuid",
                "team1_win": True,
                "team2_win": False
            }
        }

    team1_win: bool
    team2_win: bool


class BaseRoundInDB(Round, BaseInDB):
    match_id: UUID4
    set_id: UUID4
    team1_players: List[RoundPlayerInDB]
    team2_players: List[RoundPlayerInDB]


class RoundInDB(BaseRoundInDB):
    ...
