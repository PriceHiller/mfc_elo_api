from fastapi import APIRouter
from fastapi import Body
from fastapi.exceptions import HTTPException

from API.Endpoints import BaseEndpoint
from API.Schemas.user import User as UserSchema
from API.Schemas.user import UserLogin
from API.auth.jwt_handler import sign_jwt


class User(BaseEndpoint):
    route = APIRouter(prefix="/user")

    tags = ["user"]

    users = []

    @staticmethod
    @route.post("/signup", tags=tags)
    async def create_user(user: UserSchema = Body(...)):
        User.users.append(user)
        return sign_jwt(user.email)

    @staticmethod
    @route.post("/login", tags=tags)
    async def login_user(user: UserLogin = Body(...)):
        for existing_user in User.users:
            if existing_user.email == user.email and existing_user.password == user.password:
                return sign_jwt(user.email)

        raise HTTPException(status_code=403,
                            detail="Incorrect Login Credentials")
