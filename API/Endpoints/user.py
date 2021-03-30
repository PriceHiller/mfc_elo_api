import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Response
from fastapi.exceptions import HTTPException
from pydantic import UUID4

from API.Endpoints import BaseEndpoint

from API.Schemas import BaseSchema
from API.Schemas.User.user import UserCreate
from API.Schemas.User.user import UserInDBExtra

from API.Auth import JWTBearer
from API.Auth import verify_password

from API.Database.Crud.User.user import create_user
from API.Database.Crud.User.user import get_user_by_username
from API.Database.Crud.User.user import check_user

from API.Database.Crud.User.token import create_token, get_token_by_id
from API.Database.Crud.User.token import get_token_by_token
from API.Database.Crud.User.token import delete_token

log = logging.getLogger(__name__)


class User(BaseEndpoint):
    route = APIRouter(prefix="/user")

    tags = ["user"]

    @staticmethod
    @route.post("/signup", tags=tags, response_model=BaseSchema)
    async def create_user(user: UserCreate) -> BaseSchema:
        user_id = str(await create_user(user=user))
        log.info(f"The user \"{user.username}\" was created with id \"{user_id}\"")
        return BaseSchema(
            message="User Successfully Created",
            extra=[{"User ID": user_id}]
        )

    @staticmethod
    @route.post("/login", tags=tags, response_model=UserInDBExtra)
    async def login_user(response: Response, user: UserCreate) -> UserInDBExtra:
        if existing_user := await get_user_by_username(username=user.username):
            if existing_user.username == user.username and \
                    verify_password(user.password, existing_user.hashed_password):
                await check_user(user=existing_user)
                if existing_user.token:
                    if not JWTBearer.verify_jwt(existing_user.token.token):
                        token = await get_token_by_token(existing_user.token.token)
                        await delete_token(token.id)

                if not existing_user.token:
                    token_id = await create_token(existing_user)
                    token = await get_token_by_id(token_id, fetch_one=True)
                    existing_user.token = token
                    existing_user = \
                        UserInDBExtra(
                            **dict(existing_user),
                        )
                user = UserInDBExtra(
                    **dict(existing_user),
                )
                deleted_token = await JWTBearer.remove_cookie(response)
                if deleted_token:
                    token_id = await get_token_by_token(deleted_token)
                    await delete_token(token_id.token)
                await JWTBearer.grant_cookie(response, "Bearer " + user.token.token)
                log.info(f"User \"{user.username}\" ({existing_user.id}) logged in ")
                return user
        raise HTTPException(status_code=403,
                            detail="Incorrect Login Credentials")

    @staticmethod
    @route.post("/verify", tags=tags, response_model=UserInDBExtra)
    async def verify_logged_in(auth=Depends(JWTBearer())) -> UserInDBExtra:
        user = await check_user(token=auth[0], user_id=auth[-1])
        if user.is_active:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is deactivated"
            )

    @staticmethod
    @route.post("/revoke_token", tags=tags, response_model=BaseSchema)
    async def revoke_token(token_id: UUID4, auth=Depends(JWTBearer())):
        await check_user(token=auth[0], user_id=auth[-1])
        if token := await get_token_by_id(token_id, fetch_one=True):
            log.info(f"User \"{auth[-1]}\" revoked a token \"{token_id}\"")
            await delete_token(token.id)
            return BaseSchema(message="Success")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Token with id {token_id} was not found"
        )
