from fastapi.exceptions import HTTPException
from fastapi import status

from asyncpg.exceptions import UniqueViolationError

from API.Database.Models.user import User
from API.Database import BaseDB

from API.Schemas.user import UserPW as SchemaUser

from API.auth import get_password_hash

db = BaseDB.db


async def create_user(user: SchemaUser) -> dict:
    query = User.__table__.insert().values(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email=user.email
    )
    print(query)
    try:
        return await db.execute(query)  # This will return the user ID
    except UniqueViolationError:
        HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
