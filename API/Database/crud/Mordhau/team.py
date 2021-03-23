from fastapi.exceptions import HTTPException
from fastapi import status

from asyncpg.exceptions import UniqueViolationError
from asyncpg.exceptions import DataError

from API.Database.Models.Mordhau.team import Team as ModelTeam
from API.Database import BaseDB

from API.Schemas.Mordhau.team import ReturnTeam
from API.Schemas.Mordhau.team import Team as SchemaTeam

db = BaseDB.db


async def create_team(team: SchemaTeam):
    print(team)
    query = ModelTeam.__table__.insert().values(
        team_name=team.team_name,
        elo=team.elo
    )

    try:
        return await db.execute(query)
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Team already exists")


async def delete_team(team_id):
    query = ModelTeam.__table__.delete().select(
        team_id=team_id
    )

    return await db.execute(query)


async def get_teams() -> list[ReturnTeam]:
    query: ModelTeam.__table__.select = ModelTeam.__table__.select()

    if result := await db.fetch_all(query):
        teams = []
        for team in result:
            team = dict(team)
            team["id"] = str(team["id"])
            teams.append(ReturnTeam(**team))
        return teams
    return []


async def get_team_by_name(team_name: str) -> ReturnTeam:
    query: ModelTeam.__table__.select = ModelTeam.__table__.select().where(
        ModelTeam.team_name == team_name
    )

    if result := dict(await db.fetch_one(query)):
        result["id"] = str(result["id"])
        return ReturnTeam(**result)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find team: {team_name}",
        )


async def get_team_by_id(id) -> ReturnTeam:
    query: ModelTeam.__table__.select = ModelTeam.__table__.select().where(
        ModelTeam.id == id
    )
    if result := dict(await db.fetch_one(query)):
        result["id"] = str(result["id"])
        return ReturnTeam(**result)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find team: {id}",
        )


async def update_name(team_id, new_name: str):
    query: ModelTeam.__table__.update = ModelTeam.__table__.update().where(
        ModelTeam.id == team_id
    ).values(team_name=new_name)

    await db.execute(query)

    return await get_team_by_name(new_name)


async def update_elo(team_id, new_elo: int):
    query: ModelTeam.__table__.update = ModelTeam.__table__.update().where(
        ModelTeam.id == team_id
    ).values(elo=new_elo)

    await db.execute(query)

    return await get_team_by_id(team_id)
