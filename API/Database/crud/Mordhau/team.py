from fastapi.exceptions import HTTPException
from fastapi import status

from asyncpg.exceptions import UniqueViolationError
from asyncpg.exceptions import DataError

from API.Database.Models.Mordhau.team import Team as ModelTeam
from API.Database import BaseDB

from API.Schemas.Mordhau.team import Team as SchemaTeam

db = BaseDB.db


async def create_team(team: SchemaTeam):
    query = ModelTeam.__table__.insert().select(
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


async def get_team_by_name(team_name: str) -> ModelTeam:
    query: ModelTeam.__table__.select = ModelTeam.__table__.select().where(
        ModelTeam.team_name == team_name
    )

    if result := await db.fetch_one(query):
        return ModelTeam(**dict(result))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find team: {team_name}",
        )


async def get_team_by_id(id) -> [ModelTeam, str]:
    query: ModelTeam.__table__.select = ModelTeam.__table__.select().where(
        ModelTeam.id == id
    )
    try:
        if result := await db.fetch_one(query):
            return ModelTeam(**dict(result))
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not find team: {id}",
            )
    except DataError:
        return None

