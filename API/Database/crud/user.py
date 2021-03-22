from fastapi.exceptions import HTTPException
from fastapi import status

from asyncpg.exceptions import UniqueViolationError

from databases.backends.postgres import Record

from API.Database.Models.user import User as ModelUser
from API.Database import BaseDB

from API.Schemas.user import UserPW as SchemaUser

from API.auth import get_password_hash

db = BaseDB.db


async def create_user(user: SchemaUser) -> dict:
    query = ModelUser.__table__.insert().values(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email=user.email,
        is_active=True,
    )

    try:
        return await db.execute(query)  # This will return the user ID
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


async def get_user_by_username(username: str) -> ModelUser:
    query: ModelUser.__table__.select = ModelUser.__table__.select().where(
        ModelUser.username == username
    )
    if result := await db.fetch_one(query):
        result: Record
        return ModelUser(**dict(result))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find username: {username}",
        )


async def get_user_by_id(id) -> ModelUser:
    query: ModelUser.__table__.select = ModelUser.__table__.select().where(
        ModelUser.id == id
    )

    if result := await db.fetch_one(query):
        return ModelUser(**dict(result))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find user_id: {id}",
        )
