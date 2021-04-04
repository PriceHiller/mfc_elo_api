from typing import Optional
from typing import Union
from typing import List

from pydantic import Field
from pydantic import UUID4

from API.Schemas import BaseInDB
from API.Schemas import BaseSchema
from API.Schemas.Mordhau.Game.round import RoundInDB


class BaseSet(BaseSchema):
    map: str
    match_id: Union[UUID4, str, int] = Field(..., minlength=32, maxlength=36)


class Set(BaseSet):
    class Config:
        schema_extra = {
            "example": {
                "map": "skm_moshpit",
                "match_id": "uuid"
            }
        }


class BaseSetInDB(Set, BaseInDB):
    rounds: List[RoundInDB]


class SetInDB(BaseSetInDB):
    ...
