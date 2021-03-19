from fastapi.exceptions import HTTPException
from fastapi import status

from asyncpg.exceptions import UniqueViolationError

from API.Database.Models.user import User as ModelUser
from API.Database import BaseDB

from API.Schemas.user import UserPW as SchemaUser

from API.auth import get_password_hash

db = BaseDB.db


async def create_user(user: SchemaUser) -> dict:
    query = ModelUser.__table__.insert().values(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email=user.email
    )
    print(query)
    try:
        return await db.execute(query)  # This will return the user ID
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


async def get_user_by_username(username: str) -> [ModelUser, None]:
    query: ModelUser.__table__.select = ModelUser.__table__.select().where(
        ModelUser.username == username
    )

    if (result := await db.fetch_one(query)) is not None:
        return ModelUser(**dict(result))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
