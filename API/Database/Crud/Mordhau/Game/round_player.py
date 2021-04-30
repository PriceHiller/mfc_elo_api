from fastapi import HTTPException
from fastapi import status

from pydantic import UUID4
from asyncpg import DataError

from API.Database import BaseDB
from API.Database.Models.Mordhau.Game.round import RoundPlayer as ModelRoundPlayer

from API.Schemas.Mordhau.Game.round import RoundPlayerInDB as SchemaRoundPlayerInDB
from API.Schemas.Mordhau.Game.round import CreateRoundPlayer as SchemaCreateRoundPlayer
from API.Schemas.Mordhau.Game.round import CreateRoundPlayers as SchemaCreateRoundPlayers

db = BaseDB.db


async def get_round_player(
        match_schema=None,
        match_str=None,
        query=None,
        fetch_one=False
) -> [[SchemaRoundPlayerInDB], SchemaRoundPlayerInDB]:
    if query is None:
        if not match_schema or not match_str:
            raise ValueError("If query is not passed both match_schema and match_str must be passed values")
        query: ModelRoundPlayer.__table__.select = ModelRoundPlayer.__table__.select().where(
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
        return SchemaRoundPlayerInDB(
            **dict(result),
        )
    else:
        round_players = []
        for _round_player in result:
            round_players.append(
                SchemaRoundPlayerInDB(
                    **dict(_round_player)
                )
            )
        return round_players


async def get_round_players_by_round_id(round_id):
    try:
        return await get_round_player(ModelRoundPlayer.round_id, round_id, fetch_one=False)
    except DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID given"
        )


async def get_round_player_by_id(id):
    try:
        return await get_round_player(ModelRoundPlayer.player_id, id, fetch_one=False)
    except DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID given"
        )


async def get_round_played_by_id(id):
    try:
        return await get_round_player(ModelRoundPlayer.id, id, fetch_one=True)
    except DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID given"
        )


async def get_round_players() -> list[SchemaRoundPlayerInDB]:
    query: ModelRoundPlayer.__table__.select = ModelRoundPlayer.__table__.select()

    return await get_round_player(query=query, fetch_one=False)


async def get_round_player_by_player(player_id: UUID4) -> list[SchemaRoundPlayerInDB]:
    return await get_round_player(ModelRoundPlayer.player_id, player_id, fetch_one=False)


async def create_round_player(round_player: SchemaCreateRoundPlayer) -> UUID4:
    query: ModelRoundPlayer.__table__.insert = ModelRoundPlayer.__table__.insert().values(
        score=round_player.score,
        kills=round_player.kills,
        deaths=round_player.deaths,
        assists=round_player.assists,
        team_number=round_player.team_number,
        team_id=round_player.team_id,
        player_id=round_player.player_id,
        round_id=round_player.round_id
    )

    try:
        return await db.execute(query)
    except DataError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


async def create_all_round_players(round_all: SchemaCreateRoundPlayers):
    player_ids = []
    for player in round_all.round_players:
        print(player)
        player_ids.append(await create_round_player(player))

    return player_ids
