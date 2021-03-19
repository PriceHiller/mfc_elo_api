from fastapi import APIRouter, Depends
from fastapi import Body
from fastapi import Response
from fastapi import Request
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from API.Endpoints import BaseEndpoint

from API.Schemas.user import User as SchemaUser
from API.Schemas.user import UserPW

from API.auth import JWTBearer
from API.auth import verify_password

from API.Database.crud.user import create_user, get_user_by_username


class User(BaseEndpoint):
    route = APIRouter(prefix="/user")

    tags = ["user"]

    @staticmethod
    @route.post("/signup", tags=tags)
    async def create_user(user: UserPW = Body(...)):
        user_id = await create_user(user=user)
        return {"Status": "User Created", "Id": user_id}

    @staticmethod
    @route.post("/login", tags=tags)
    async def login_user(response: Response, user: UserPW = Body(...)):
        if existing_user := await get_user_by_username(username=user.username):
            if existing_user.username == user.username and \
                    verify_password(user.password, existing_user.hashed_password):
                jwt = JWTBearer.sign_jwt(user.username)
                await JWTBearer.grant_cookie(response, jwt)
                return {"token": jwt}
        raise HTTPException(status_code=403,
                            detail="Incorrect Login Credentials")

    @staticmethod
    @route.post("/verify", tags=tags)
    async def read_private(user: SchemaUser = Depends(JWTBearer())):
        return {"username": user, "user status": "good"}
