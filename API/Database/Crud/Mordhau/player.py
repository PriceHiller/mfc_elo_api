from fastapi.exceptions import HTTPException
from fastapi import status

from asyncpg.exceptions import UniqueViolationError
from databases.backends.postgres import Record

from API.Database.Models.Mordhau.player import Player as ModelPlayer
from API.Database import BaseDB

from API.Schemas.Mordhau.player import Player as SchemaPlayer
from API.Schemas.Mordhau.player import PlayerInDB as SchemaPlayerInDB

db = BaseDB.db


async def create_player(player: SchemaPlayer) -> str:
    query: ModelPlayer.__table__.select = ModelPlayer.__table__.insert().values(
        player_name=player.player_name,
        playfab_id=player.playfab_id,
        discord_id=player.discord_id
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


async def get_player_by_name(player_name: str) -> SchemaPlayerInDB:
    query: ModelPlayer.__table__.select = ModelPlayer.__table__.select().where(
        ModelPlayer.player_name == player_name
    )

    if result := await db.fetch_one(query):
        return SchemaPlayerInDB(**dict(result))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find player: {player_name}",
        )


async def get_player_by_id(id) -> SchemaPlayerInDB:
    query: ModelPlayer.__table__.select = ModelPlayer.__table__.select().where(
        ModelPlayer.id == id
    )

    if result := dict(await db.fetch_one(query)):
        return SchemaPlayerInDB(**result)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find player: {id}",
        )


async def get_players() -> list[SchemaPlayerInDB]:
    query: ModelPlayer.__table__.select = ModelPlayer.__table__.select()

    if result := await db.fetch_all(query):
        return [SchemaPlayerInDB(**dict(player)) for player in result]
    return []


async def get_players_by_team_id(team_id) -> [SchemaPlayerInDB]:
    query: ModelPlayer.__table__.select = ModelPlayer.__table__.select().where(
        ModelPlayer.team_id == team_id
    )

    if result := await db.fetch_all(query):
        return [SchemaPlayerInDB(**dict(player)) for player in result]
    return []


async def update_player_discord_id(player_id, new_discord_id):
    query: ModelPlayer.__table__.update = ModelPlayer.__table__.update().where(
        ModelPlayer.id == player_id
    ).values(discord_id=new_discord_id)

    return await db.execute(query)
