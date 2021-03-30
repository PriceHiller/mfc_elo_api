from fastapi import HTTPException
from fastapi import status

from asyncpg import DataError

from API.Database import BaseDB
from API.Database.Models.Mordhau.Game.match import Match as ModelMatch
from API.Database.Crud.Mordhau.Game.set import get_sets_by_match_id

from API.Schemas.Mordhau.Game.match import MatchInDB as SchemaMatchInDB
from API.Schemas.Mordhau.Game.match import StrippedMatchInDB as SchemaStrippedMatchInDB
from API.Schemas.Mordhau.Game.match import CreateMatch as SchemaCreateMatch

db = BaseDB.db


async def get_match(
        match_schema=None,
        match_str=None,
        query=None,
        fetch_one=False
) -> [[SchemaMatchInDB], SchemaMatchInDB]:

    if query is None:
        if not match_schema or not match_str:
            raise ValueError("If query is not passed both match_schema and match_str must be passed values")
        query: ModelMatch.__table__.select = ModelMatch.__table__.select().where(
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

    if fetch_one:
        stripped_match = SchemaStrippedMatchInDB(**dict(result))
        sets = await get_sets_by_match_id(stripped_match.id)
        return SchemaMatchInDB(
            **dict(stripped_match),
            sets=sets
        )
    else:
        matches = []
        for _match in result:
            single_match = SchemaStrippedMatchInDB(**dict(_match))
            sets = await get_sets_by_match_id(single_match.id)
            matches.append(
                SchemaMatchInDB(
                    **dict(single_match),
                    sets=sets
                )
            )
        return matches


async def get_match_by_id(match_id) -> SchemaMatchInDB:
    try:
        return await get_match(ModelMatch.id, match_id, fetch_one=True)
    except DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID given"
        )


async def get_matches_by_team_ids(team1_id, team2_id) -> [SchemaMatchInDB]:
    query: ModelMatch.__table__.select = ModelMatch.__table__.select().where(
        ModelMatch.team1_id == team1_id,
        ModelMatch.team2_id == team2_id
    )
    return await get_match(query=query, fetch_one=False)


async def get_matches_by_team_id(team_id) -> [SchemaMatchInDB]:
    if result := await get_match(match_schema=ModelMatch.team1_id, match_str=team_id, fetch_one=False):
        return result
    else:
        return await get_match(match_schema=ModelMatch.team2_id, match_str=team_id, fetch_one=False)


async def get_matches() -> list[SchemaMatchInDB]:
    query: ModelMatch.__table__.select = ModelMatch.__table__.select()

    return await get_match(query=query, fetch_one=False)


async def create_match(match: SchemaCreateMatch):
    query: ModelMatch.__table__.insert = ModelMatch.__table__.insert().values(
        team1_id=match.team1_id,
        team2_id=match.team2_id
    )

    return await db.execute(query)
