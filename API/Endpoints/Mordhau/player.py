import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from API.auth import JWTBearer

from API.Endpoints import BaseEndpoint

from API.Database.crud.Mordhau.player import get_players
from API.Database.crud.Mordhau.player import get_player_by_id
from API.Database.crud.Mordhau.player import get_player_by_name
from API.Database.crud.Mordhau.player import create_player
from API.Database.crud.Mordhau.player import delete_player

from API.Schemas.Mordhau.player import Player as MordhauPlayer

log = logging.getLogger(__name__)


class MordhauPlayer(BaseEndpoint):
    tags = ["mordhau", "mordhau-player"]

    route = APIRouter(prefix="/player")

    @staticmethod
    @route.get("/", tags=tags)
    async def player():
        return await get_players()

    @staticmethod
    @route.get("/id", tags=tags)
    async def _id(id: str) -> [MordhauPlayer, dict]:
        if player := await get_player_by_id(id):
            return player
        return {}

    @staticmethod
    @route.get("/name", tags=tags)
    async def name(player_name: str) -> [MordhauPlayer, dict]:
        if player := await get_player_by_name(player_name):
            return player
        return {}

    @staticmethod
    @route.post("/create", tags=tags)
    async def create(player: MordhauPlayer, auth=Depends(JWTBearer())) -> dict[str, str]:
        log.info(f"User id \"{auth[-1]}\" issued a creation of Mordhau Player \"{player.player_name}\"")
        return {"Player ID": await create_player(player)}

    @staticmethod
    @route.post("/delete", tags=tags)
    async def delete(player_id: str = Query(None, min_length=32, max_length=36), auth=Depends(JWTBearer())):

        if player_id and await get_player_by_id(player_id):
            log.info(f"User id \"{auth[-1]}\" issued a delete of Mordhau Player id \"{player_id}\"")
            await delete_player(player_id)
            return {"Deleted player": player_id}