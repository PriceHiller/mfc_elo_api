import logging

import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from fastapi.exceptions import HTTPException

from pydantic import UUID4

from API.Auth import JWTBearer

from API.Database.Crud.Mordhau.Game.round import get_round_by_id
from API.Database.Crud.Mordhau.Game.round import get_rounds_by_set_id
from API.Database.Crud.Mordhau.Game.round import get_rounds
from API.Database.Crud.Mordhau.Game.round import create_round

from API.Database.Crud.Mordhau.Game.round_player import get_round_player_by_id
from API.Database.Crud.Mordhau.Game.round_player import get_round_players
from API.Database.Crud.Mordhau.Game.round_player import create_round_player
from API.Database.Crud.Mordhau.Game.round_player import create_all_round_players

from API.Schemas import BaseSchema
from API.Schemas.Mordhau.Game.round import RoundInDB
from API.Schemas.Mordhau.Game.round import CreateRound
from API.Schemas.Mordhau.Game.round import RoundPlayerInDB
from API.Schemas.Mordhau.Game.round import CreateRoundPlayer
from API.Schemas.Mordhau.Game.round import CreateRoundPlayers

from API.Endpoints import BaseEndpoint

log = logging.getLogger(__name__)


class Round(BaseEndpoint):
    tags = ["mordhau-round"]

    route = APIRouter(prefix="/round")

    @staticmethod
    @route.get("/round-id", tags=tags, response_model=RoundInDB)
    async def get_round_by_id(id):
        return await get_round_by_id(id)

    @staticmethod
    @route.get("/by-set-id", tags=tags, response_model=list[RoundInDB])
    async def get_round_by_set_id(set_id):
        return await get_rounds_by_set_id(set_id)

    @staticmethod
    @route.get("/round-all", tags=tags, response_model=list[RoundInDB])
    async def get_all_rounds():
        return await get_rounds()

    @staticmethod
    @route.post("/create-round", tags=tags, response_model=BaseSchema)
    async def create_round(round: CreateRound):
        round_id = await create_round(round)
        return BaseSchema(
            message=f"Created round with id {round_id}",
            extra=[
                {
                    "round_id": round_id
                }
            ]
        )

    @staticmethod
    @route.get("/round-player-id", tags=tags, response_model=RoundPlayerInDB)
    async def get_round_player_by_id(round_player_id):
        return await get_round_player_by_id(round_player_id)

    @staticmethod
    @route.get("/round-players-all", tags=tags, response_model=list[RoundPlayerInDB])
    async def get_all_round_players():
        return await get_round_players()

    @staticmethod
    @route.post("/create-round-player", tags=tags, response_model=BaseSchema)
    async def create_round_player(round_player: CreateRoundPlayer):
        return await create_round_player(round_player)

    @staticmethod
    @route.post("/create-all-round-players", tags=tags, response_model=BaseSchema)  # Shit endpoint name, pls god rename
    async def create_round_all(round_players: CreateRoundPlayers):
        print(round_players)
        round_player_ids = [str(round_player_id) for round_player_id in await create_all_round_players(round_players)]
        return BaseSchema(
            message=f"Created round with round players, ids: {', '.join(round_player_ids)}",
            extra=[
                {
                    "round_player_ids": round_player_ids
                }
            ]
        )
