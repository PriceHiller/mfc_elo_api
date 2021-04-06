from asyncpg import UniqueViolationError, DataError
from databases.backends.postgres import Record
from fastapi import status
from fastapi.exceptions import HTTPException

from API.Database import BaseDB
from API.Database.Models.User.tokens import Token as ModelToken

from API.Schemas.User.token import TokenInDB as SchemaTokenInDB
from API.Schemas.User.user import UserInDB as SchemaUserInDB

from API.Auth import JWTBearer

db = BaseDB.db


async def get_token(match_schema, match_str, fetch_one=False) -> [[SchemaTokenInDB], SchemaTokenInDB]:
    query: ModelToken.__table__.select = ModelToken.__table__.select().where(
        match_schema == match_str
    )

    result: Record

    if fetch_one:
        result = await db.fetch_one(query)
    else:
        result = await db.fetch_all(query)

    if result:
        if fetch_one:
            return SchemaTokenInDB(**dict(result))
        else:
            return [SchemaTokenInDB(**dict(token)) for token in result]


async def create_token(user: SchemaUserInDB) -> str:
    if user.token:
        token = user.token
        if "Bearer" in user.token.token:
            token = user.token.token.split("Bearer")[-1].strip()
    else:
        token = JWTBearer.sign_jwt(user.id).split("Bearer")[-1].strip()

    query: ModelToken.__table__.insert = ModelToken.__table__.insert().values(
        token=token,
        user_id=user.id
    )

    try:
        return await db.execute(query)
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Token already exists")


async def get_token_by_id(token_id, fetch_one=True) -> SchemaTokenInDB:
    token_id = str(token_id)
    if len(token_id) < 32 or len(token_id) > 36:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Length of token_id is less than 32 or more than 36."
        )
    try:
        return await get_token(ModelToken.id, token_id, fetch_one=fetch_one)
    except DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID given"
        )


async def get_token_by_token(token: str) -> SchemaTokenInDB:
    if "Bearer" in token:
        token = token.split("Bearer")[-1].strip()

    return await get_token(ModelToken.token, token, fetch_one=True)


async def get_token_by_user_id(id, fetch_one=False) -> SchemaTokenInDB:
    return await get_token(ModelToken.user_id, id, fetch_one=fetch_one)


async def delete_token(token_id: str) -> str:
    query: ModelToken.__table__.delete = ModelToken.__table__.delete().where(
        ModelToken.id == token_id
    )

    return await db.execute(query)
