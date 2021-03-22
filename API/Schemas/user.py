from typing import Optional
from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


class BaseUser(BaseModel):
    username: str = Field(min_length=3,
                          max_length=36)
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True


class UserPW(BaseUser):
    password: str = Field(min_length=8,
                          regex=R"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

    class Config:
        schema_extra = {
            "example": {
                "username": "John Smith",
                "email": "johnsmith@email.com",
                "password": "SomeSecurePassword@321"
            }
        }


class JWTUser(BaseUser):
    id: Any
    is_active: bool
    token: str
