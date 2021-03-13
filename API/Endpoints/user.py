from fastapi import APIRouter, Depends
from fastapi import Body
from fastapi import Response
from fastapi.exceptions import HTTPException

from API.Endpoints import BaseEndpoint
from API.Endpoints import CommonTags

from API.Schemas.user import User as UserSchema

from API.auth import JWTBearer
from API.auth import check_authentication
from API.auth import users
from API.auth import get_password_hash
from API.auth import verify_password


class User(BaseEndpoint):
    route = APIRouter(prefix="/user")

    tags = ["user"]

    @staticmethod
    @route.post("/signup", tags=tags)
    async def create_user(user: UserSchema = Body(...)):
        user.password = get_password_hash(user.password)
        users.append(user)
        return JWTBearer.sign_jwt(user.email)

    @staticmethod
    @route.post("/login", tags=tags)
    async def login_user(response: Response, user: UserSchema = Body(...)):
        for existing_user in users:
            if existing_user.email == user.email and verify_password(user.password, existing_user.password):
                token = JWTBearer.sign_jwt(user.email)
                response.set_cookie("session", token["token"])
                return JWTBearer.sign_jwt(user.email)
        raise HTTPException(status_code=403,
                            detail="Incorrect Login Credentials")

    @staticmethod
    @route.post("/private", tags=[CommonTags.jwt, CommonTags.jwt, CommonTags.auth_required, "user"])
    async def read_private(user: UserSchema = Depends(check_authentication)):
        return {"username": user, "private": "private data"}
