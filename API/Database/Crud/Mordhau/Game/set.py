from fastapi import HTTPException
from fastapi import status

from asyncpg import DataError

from API.Database import BaseDB
from API.Database.Models.Mordhau.Game.set import Set as ModelSet

from API.Schemas.Mordhau.Game.set import SetInDB as SchemaSetInDB
from API.Schemas.Mordhau.Game.set import Set as SchemaSet

db = BaseDB.db


async def get_set(
        match_schema=None,
        match_str=None,
        query=None,
        fetch_one=False
) -> [list[SchemaSetInDB], SchemaSetInDB]:
    if query is None:
        if not match_schema or not match_str:
            raise ValueError("If query is not passed both match_schema and match_str must be passed values")
        query: ModelSet.__table__.select = ModelSet.__table__.select().where(
            match_schema == match_str
        )

    if fetch_one:
        result = await db.fetch_one(query)
        if not result:
            return None
    else:
        result = await db.fetch_all(query)
        if not result:
            return []

    from API.Database.Crud.Mordhau.Game.round import get_rounds_by_set_id

    if fetch_one:
        set = dict(result)
        rounds = await get_rounds_by_set_id(set["id"])
        return SchemaSetInDB(
            **set,
            rounds=rounds
        )
    else:
        sets = []
        for _set in result:
            set = dict(_set)
            rounds = await get_rounds_by_set_id(set["id"])
            sets.append(
                SchemaSetInDB(
                    **set,
                    rounds=rounds
                )
            )
        return sets


async def get_set_by_id(set_id) -> SchemaSetInDB:
    try:
        return await get_set(ModelSet.id, set_id, fetch_one=True)
    except DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID given"
        )


async def get_sets_by_match_id(match_id) -> list[SchemaSetInDB]:
    try:
        return await get_set(ModelSet.match_id, match_id, fetch_one=False)
    except DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )


async def get_sets_by_map(map_name: str) -> list[SchemaSetInDB]:
    return await get_set(ModelSet.map, map_name.casefold(), fetch_one=True)


async def get_sets() -> list[SchemaSetInDB]:
    query: ModelSet.__table__.select = ModelSet.__table__.select()

    return await get_set(query=query, fetch_one=False)


async def create_set(set: SchemaSet):
    query: ModelSet.__table__.insert = ModelSet.__table__.insert().values(
        map=set.map.casefold(),
        match_id=set.match_id
    )

    return await db.execute(query)
