from fastapi.exceptions import HTTPException
from fastapi import status

from asyncpg.exceptions import UniqueViolationError
from databases.backends.postgres import Record

from API.Database.Models.Mordhau.player import Player as ModelPlayer
from API.Database import BaseDB

from API.Schemas.Mordhau.player import Player as SchemaPlayer

from .team import get_team_by_id

db = BaseDB.db


async def create_player(player: SchemaPlayer) -> str:
    if player.team_id:
        team = await get_team_by_id(player.team_id)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Team with ID {player.team_id} not found")
        player.team_id = str(team.id)
        print(player)
        print(player.team_id)
        query = ModelPlayer.__table__.insert().values(
            player_name=player.player_name,
            playfab_id=player.playfab_id,
            steam64=player.steam64,
            team_id=player.team_id
        )
    else:
        query: ModelPlayer.__table__.select = ModelPlayer.__table__.insert().values(
            player_name=player.player_name,
            playfab_id=player.playfab_id,
            steam64=player.steam64,
        )

    try:
        return await db.execute(query)
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Player already exists")


async def delete_player(player_id):
    query: ModelPlayer.__table__.delete = ModelPlayer.__table__.delete(
        ModelPlayer.id == player_id
    )

    return await db.execute(query)


async def get_player_by_name(player_name: str) -> SchemaPlayer:
    query: ModelPlayer.__table__.select = ModelPlayer.__table__.select().where(
        ModelPlayer.player_name == player_name
    )

    if result := await db.fetch_one(query):
        result: Record
        return SchemaPlayer(**dict(result))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find player: {player_name}",
        )


async def get_player_by_id(id) -> SchemaPlayer:
    query: ModelPlayer.__table__.select = ModelPlayer.__table__.select().where(
        ModelPlayer.id == id
    )

    if result := await db.fetch_one(query):
        result: Record
        return SchemaPlayer(**dict(result))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find player: {id}",
        )


async def get_players():
    query: ModelPlayer.__table__.select = ModelPlayer.__table__.select()

    if result := await db.fetch_all(query):
        players = []
        for player in result:
            player = dict(player)
            player["id"] = str(player["id"])
            players.append(player)
        return players
    return []
