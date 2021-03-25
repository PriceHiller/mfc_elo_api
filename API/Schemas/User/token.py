from pydantic import BaseModel

from API.Schemas import BaseInDB

class BaseToken(BaseModel):
    token: str


class Token(BaseToken):
    ...


class BaseTokenInDB(BaseToken, BaseInDB):
    ...

class TokenInDB(BaseTokenInDB):
    ...
