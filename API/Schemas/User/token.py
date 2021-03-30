from API.Schemas import BaseInDB
from API.Schemas import BaseSchema


class BaseToken(BaseSchema):
    token: str


class Token(BaseToken):
    ...

    class Config:
        schema_extra = {
            "example": {
                "token": "sometoken",
            }
        }


class BaseTokenInDB(BaseToken, BaseInDB):
    ...


class TokenInDB(BaseTokenInDB):
    ...
