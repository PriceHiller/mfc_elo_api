import logging

from fastapi import APIRouter, Depends
from fastapi import Body
from fastapi import Response
from fastapi.exceptions import HTTPException

from API.Endpoints import BaseEndpoint

from API.Schemas.user import JWTUser
from API.Schemas.user import UserPW

from API.auth import JWTBearer
from API.auth import verify_password

from API.Database.crud.user import create_user
from API.Database.crud.user import get_user_by_username
from API.Database.crud.user import get_user_by_id

log = logging.getLogger(__name__)

class User(BaseEndpoint):
    route = APIRouter(prefix="/user")

    tags = ["user"]

    @staticmethod
    @route.post("/signup", tags=tags, response_model=dict)
    async def create_user(user: UserPW = Body(...)):
        user_id = await create_user(user=user)
        log.info(f"The user \"{user.username}\" was created with id \"{user_id}\"")
        return {"Status": "User Created", "Id": user_id}

    @staticmethod
    @route.post("/login", tags=tags, response_model=JWTUser)
    async def login_user(response: Response, user: UserPW = Body(...)) -> JWTUser:
        if existing_user := await get_user_by_username(username=user.username):

            if existing_user.username == user.username and \
                    verify_password(user.password, existing_user.hashed_password):
                jwt = JWTBearer.sign_jwt(str(existing_user.id))
                user = JWTUser(
                    id=str(existing_user.id),
                    username=existing_user.username,
                    email=existing_user.email,
                    is_active=bool(existing_user.is_active),
                    token=jwt
                )
                await JWTBearer.grant_cookie(response, jwt)
                log.info(f"User \"{user.username}\" ({user.id}) logged in ")
                return user
        raise HTTPException(status_code=403,
                            detail="Incorrect Login Credentials")

    @staticmethod
    @route.post("/verify", tags=tags, response_model=JWTUser)
    async def read_private(auth=Depends(JWTBearer())) -> JWTUser:
        user = await get_user_by_id(auth[-1])
        user = JWTUser(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            token=auth[-1]
        )
        return user
