from typing import Optional
from typing import Union
from typing import List

from pydantic import Field
from pydantic import UUID4

from API.Schemas import BaseInDB
from API.Schemas import BaseSchema
from API.Schemas.Mordhau.Game.set import SetInDB


class BaseMatch(BaseSchema):
    team1_id: Optional[Union[UUID4, str, int]] = Field(..., minlength=32, maxlength=36)
    team2_id: Optional[Union[UUID4, str, int]] = Field(..., minlength=32, maxlength=36)


class Match(BaseMatch):
    class Config:
        schema_extra = {
            "example": {
                "team1_id": "uuid",
                "team2_id": "uuid"
            }
        }


class BaseMatchInDB(Match, BaseInDB):
    ...


class MatchInDB(BaseMatchInDB):
    sets: List[SetInDB]
