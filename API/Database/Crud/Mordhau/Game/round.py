from fastapi import HTTPException
from fastapi import status

from asyncpg import DataError

from API.Database import BaseDB
from API.Database.Models.Mordhau.Game.round import Round as ModelRound
from API.Database.Crud.Mordhau.Game.round_player import get_round_players_by_round_id
from API.Database.Crud.Mordhau.Game.round_player import create_round_player

from API.Schemas.Mordhau.Game.round import RoundInDB as SchemaRoundInDB
from API.Schemas.Mordhau.Game.round import CreateRound as SchemaCreateRound
from API.Schemas.Mordhau.Game.round import StrippedRoundInDB as SchemaStrippedRoundInDB

from API.Schemas.Mordhau.Game.round import RoundPlayerInDB as SchemaRoundPlayerInDB

db = BaseDB.db


def parse_rounds(round_players: list[SchemaRoundPlayerInDB]) -> \
        [list[SchemaRoundPlayerInDB], list[SchemaRoundPlayerInDB]]:
    team1 = []
    team2 = []

    if not round_players:
        return [], []
    for round_player in round_players:
        if round_player.team_number == 0:
            team1.append(round_player)
        else:
            team2.append(round_player)

    return team1, team2


async def get_round(
        match_schema=None,
        match_str=None,
        query=None,
        fetch_one=False
) -> [[SchemaRoundInDB], SchemaRoundInDB]:
    if query is None:
        if not match_schema or not match_str:
            raise ValueError("If query is not passed both match_schema and match_str must be passed values")
        query: ModelRound.__table__.select = ModelRound.__table__.select().where(
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
        stripped_round = SchemaStrippedRoundInDB(**dict(result))
        round_players = await get_round_players_by_round_id(stripped_round.id)
        team1_players, team2_players = parse_rounds(round_players)

        return SchemaRoundInDB(
            **dict(stripped_round),
            team1_players=team1_players,
            team2_players=team2_players
        )
    else:
        rounds = []
        for _round in result:
            single_round = SchemaStrippedRoundInDB(**dict(_round))
            round_players = await get_round_players_by_round_id(single_round.id)
            print(round_players)
            team1_players, team2_players = parse_rounds(round_players)
            rounds.append(
                SchemaRoundInDB(
                    **dict(single_round),
                    team1_players=team1_players,
                    team2_players=team2_players
                )
            )
        return rounds


async def get_round_by_id(round_id) -> SchemaRoundInDB:
    try:
        return await get_round(ModelRound.id, round_id, fetch_one=True)
    except DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID given"
        )


async def get_rounds_by_set_id(set_id) -> [SchemaRoundInDB]:
    try:
        return await get_round(ModelRound.set_id, set_id, fetch_one=False)
    except DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID given"
        )


async def get_rounds() -> list[SchemaRoundPlayerInDB]:
    query: ModelRound.__table__.select = ModelRound.__table__.select()

    return await get_round(query=query, fetch_one=False)


async def create_round(round: SchemaCreateRound):
    query: ModelRound.__table__.insert = ModelRound.__table__.insert().values(
        set_id=round.set_id,
        team1_win=round.team1_win,
        team2_win=round.team2_win
    )

    return await db.execute(query)



