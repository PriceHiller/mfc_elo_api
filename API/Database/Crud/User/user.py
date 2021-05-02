from fastapi.exceptions import HTTPException
from fastapi import status

from asyncpg.exceptions import UniqueViolationError

from databases.backends.postgres import Record

from API.Database.Models.User.user import User as ModelUser

from API.Database import BaseDB

from API.Schemas.User.user import UserCreate as SchemaUserCreate
from API.Schemas.User.user import UserInDB as SchemaUserInDB
from API.Schemas.User.user import UserInDBPassword as SchemaUserInDBPassword

from .token import create_token
from .token import get_token_by_user_id
from .token import get_token_by_token

from API.Auth import get_password_hash

db = BaseDB.db


async def create_user(user: SchemaUserCreate) -> str:
    """
    Creates a user and returns their UUID
    """

    query = ModelUser.__table__.insert().values(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email=user.email,
        is_active=True,
    )

    try:
        user_id = await db.execute(query)
        user = await get_user_by_id(user_id)
        await create_token(user)
        return user_id
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


async def get_user_by_username(username: str) -> SchemaUserInDBPassword:
    query: ModelUser.__table__.select = ModelUser.__table__.select().where(
        ModelUser.username == username
    )
    if result := await db.fetch_one(query):
        result: Record
        result_dict = dict(result)
        result_dict["id"] = result_dict["id"]
        return SchemaUserInDBPassword(
            **result_dict,
            token=await get_token_by_user_id(result_dict["id"], fetch_one=True)
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find username: {username}",
        )


async def get_user_by_id(id) -> SchemaUserInDB:
    user_query: ModelUser.__table__.select = ModelUser.__table__.select().where(
        ModelUser.id == id
    )

    if user := await db.fetch_one(user_query):
        result_dict = dict(user)
        result_dict["id"] = str(result_dict["id"])
        token = await get_token_by_user_id(id, fetch_one=True)
        result_dict["token"] = token
        return SchemaUserInDB(**result_dict)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find user_id: {id}",
        )


async def check_user(token=None, user_id: str = None, user: SchemaUserInDB = None):
    if token:
        if not await get_token_by_token(token.credentials):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token does not exist"
            )
    if user_id:
        try:
            user = await get_user_by_id(user_id)
            if user.is_active:
                return user
            else:
                raise HTTPException(status_code=403)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not found or not logged in"
            )
    else:
        if user.is_active:
            return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is deactivated"
    )
