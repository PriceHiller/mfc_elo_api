from typing import Optional
from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

from API.Schemas import BaseInDB
from API.Schemas import BaseSchema

from .token import TokenInDB


class BaseUser(BaseSchema):
    username: str = Field(min_length=3,
                          max_length=36)

    class Config:
        orm_mode = True


class User(BaseUser):
    ...


class UserCreate(BaseUser):
    password: str = Field(min_length=8,
                          regex=R"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

    class Config:
        schema_extra = {
            "example": {
                "username": "John Smith",
                "password": "SomeSecurePassword4321@"
            }
        }


class UpdatePW:
    password: str = Field(min_length=8,
                          regex=R"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")


class BaseUserInDB(BaseUser, BaseInDB):
    username: str


class UserInDB(BaseUserInDB):
    token: Optional[TokenInDB] = None
    email: Optional[str] = None
    is_active: bool


class UserInDBPassword(UserInDB):
    hashed_password: str
