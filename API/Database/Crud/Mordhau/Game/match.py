from fastapi import HTTPException
from fastapi import status

from asyncpg import DataError

from API.Database import BaseDB
from API.Database.Models.Mordhau.Game.match import Match as ModelMatch
from API.Database.Crud.Mordhau.Game.set import get_sets_by_match_id

# Elo calculation related imports
from API.Database.Crud.Mordhau.team import get_team_by_id
from API.Database.Crud.Mordhau.team import update_elo
from API.ELO.team import Team as ELOTeam
from API.ELO import ELO

from API.Schemas.Mordhau.Game.match import MatchInDB as SchemaMatchInDB
from API.Schemas.Mordhau.Game.match import Match as SchemaMatch

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
        match = dict(result)
        sets = await get_sets_by_match_id(match["id"])
        return SchemaMatchInDB(
            **match,
            sets=sets
        )
    else:
        matches = []
        for _match in result:
            single_match = dict(_match)
            sets = await get_sets_by_match_id(single_match["id"])
            matches.append(
                SchemaMatchInDB(
                    **single_match,
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


async def create_match(match: SchemaMatch):
    query: ModelMatch.__table__.insert = ModelMatch.__table__.insert().values(
        team1_id=match.team1_id,
        team2_id=match.team2_id,
        elo_calculated=False
    )

    return await db.execute(query)


async def calculate_elo(match_id) -> [dict[str, float], str]:
    match = await get_match(match_schema=ModelMatch.id, match_str=match_id, fetch_one=True)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find match with id {match_id}"
        )

    team1 = await get_team_by_id(match.team1_id)
    team2 = await get_team_by_id(match.team2_id)
    
    team1_rounds_won = 0
    team2_rounds_won = 0
    
    for set in match.sets:
        for _round in set.rounds:
            if _round.team1_win:
                team1_rounds_won += 1
            else:
                team2_rounds_won += 1
    
    team1_elo = ELOTeam(elo=team1.elo, rounds_won=team1_rounds_won)
    team2_elo = ELOTeam(elo=team2.elo, rounds_won=team2_rounds_won)

    if team1_rounds_won != team2_rounds_won:
        new_elo = ELO().calculate(team1_elo, team2_elo)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to calculate elo, scores were the same!"
        )
    
    await update_elo(match.team1_id, round(new_elo["team1"]))
    await update_elo(match.team2_id, round(new_elo["team2"]))

    query: ModelMatch.__table__.update = ModelMatch.__table__.update().where(
        ModelMatch.id == match_id,
    ).values(elo_calculated=True)

    await db.execute(query)

    return new_elo