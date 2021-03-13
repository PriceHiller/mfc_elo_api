from fastapi import APIRouter

from API.Endpoints import BaseEndpoint
from API.Schemas.Mordhau.player import Player as MordhauPlayer


class Mordhau(BaseEndpoint):
    route = APIRouter()

    @staticmethod
    @route.post("/player/")
    async def get_player(player: MordhauPlayer):
        return player
