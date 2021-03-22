from fastapi import APIRouter

from API.Endpoints import BaseEndpoint

from API.Database.crud.Mordhau.player import get_players


class MordhauPlayer(BaseEndpoint):
    tags = ["mordhau"]

    route = APIRouter(prefix="/player")

    @staticmethod
    @route.get("/", tags=tags)
    async def player():
        return await get_players()
