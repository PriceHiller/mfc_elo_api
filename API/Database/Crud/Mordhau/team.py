from fastapi.exceptions import HTTPException
from fastapi import status

from asyncpg.exceptions import UniqueViolationError

from API.Database.Models.Mordhau.team import Team as ModelTeam
from API.Database.Models.Mordhau.player import Player as ModelPlayer

from API.Database import BaseDB

from API.Schemas.Mordhau.team import TeamInDB as SchemaTeamInDB
from API.Schemas.Mordhau.team import Team as SchemaTeam

from .player import get_player_by_id
from .player import get_players_by_team_id

db = BaseDB.db


async def get_team(
        match_schema=None,
        match_str=None,
        query=None,
        fetch_one=False
) -> [[SchemaTeamInDB], SchemaTeamInDB]:
    if query is None:
        if not match_schema or not match_str:
            raise ValueError("If query is not passed both match_schema and match_str must be passed values")
        query: ModelTeam.__table__.select = ModelTeam.__table__.select().where(
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
        team = dict(result)
        players = await get_players_by_team_id(team["id"])

        return SchemaTeamInDB(
            **team,
            players=players
        )
    else:
        teams = []
        for _team in result:
            single_team = dict(_team)
            players = await get_players_by_team_id(single_team["id"])
            teams.append(
                SchemaTeamInDB(
                    players=players,
                    **single_team,
                )
            )
        return teams


async def create_team(team: SchemaTeam):
    query = ModelTeam.__table__.insert().values(
        team_name=team.team_name,
        elo=team.elo
    )

    try:
        return await db.execute(query)
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Team already exists")


async def delete_team(team_id):
    query = ModelTeam.__table__.delete().where(
        ModelTeam.id == team_id
    )

    await db.execute(query)


async def get_teams() -> list[SchemaTeamInDB]:
    query: ModelTeam.__table__.select = ModelTeam.__table__.select()

    return await get_team(query=query, fetch_one=False)


async def get_team_by_name(team_name: str) -> SchemaTeamInDB:
    if result := await get_team(match_schema=ModelTeam.team_name, match_str=team_name, fetch_one=True):
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find team: {team_name}",
        )


async def get_team_by_id(id) -> SchemaTeamInDB:
    if result := await get_team(match_schema=ModelTeam.id, match_str=id, fetch_one=True):
        return SchemaTeamInDB(**dict(result))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find team: {id}",
        )


async def update_name(team_id, new_name: str) -> SchemaTeamInDB:
    query: ModelTeam.__table__.update = ModelTeam.__table__.update().where(
        ModelTeam.id == team_id
    ).values(team_name=new_name.lower())

    await db.execute(query)

    return await get_team_by_name(new_name.lower())


async def update_elo(team_id, new_elo: int) -> SchemaTeamInDB:
    query: ModelTeam.__table__.update = ModelTeam.__table__.update().where(
        ModelTeam.id == team_id
    ).values(elo=new_elo)

    await db.execute(query)

    return await get_team_by_id(team_id)


async def add_player_to_team(player_id, team_id) -> SchemaTeamInDB:
    player = await get_player_by_id(player_id)
    team = await get_team_by_id(team_id)

    query: ModelPlayer.__table__.update = ModelPlayer.__table__.update().where(
        ModelPlayer.id == player.id
    ).values(team_id=team.id)

    await db.execute(query)

    return await get_team_by_id(team_id)


async def remove_player_from_team(player_id, team_id) -> SchemaTeamInDB:
    player = await get_player_by_id(player_id)
    await get_team_by_id(team_id)

    query: ModelPlayer.__table__.update = ModelPlayer.__table__.update().where(
        ModelPlayer.id == player.id
    ).values(team_id=None)

    await db.execute(query)

    return await get_team_by_id(player.id)
