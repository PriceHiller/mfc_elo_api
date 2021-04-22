import logging

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status
from fastapi.exceptions import HTTPException

from pydantic import UUID4

from API.Database.Crud.User.user import check_user
from API.Auth import JWTBearer

from API.Endpoints import BaseEndpoint

from API.Database.Crud.Mordhau.player import get_players
from API.Database.Crud.Mordhau.player import get_player_by_id
from API.Database.Crud.Mordhau.player import get_player_by_discord_id
from API.Database.Crud.Mordhau.player import get_player_by_name
from API.Database.Crud.Mordhau.player import create_player
from API.Database.Crud.Mordhau.player import delete_player
from API.Database.Crud.Mordhau.player import update_player_discord_id
from API.Database.Crud.Mordhau.player import get_player_by_playfab_id
from API.Database.Crud.Mordhau.player import make_ambassador
from API.Database.Crud.Mordhau.player import remove_ambassador
from API.Database.Crud.Mordhau.player import update_player_name

from API.Schemas.Mordhau.player import Player
from API.Schemas.Mordhau.player import PlayerInDB
from API.Schemas import BaseSchema

log = logging.getLogger(__name__)


class MordhauPlayer(BaseEndpoint):
    tags = ["mordhau-player"]

    route = APIRouter(prefix="/player")

    @staticmethod
    @route.get("/all", tags=tags, response_model=List[PlayerInDB])
    async def player():
        return await get_players()

    @staticmethod
    @route.get("/id", tags=tags, response_model=PlayerInDB)
    async def _id(id: UUID4) -> [Player, dict]:
        if player := await get_player_by_id(id):
            return player
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {id} not found"
        )

    @staticmethod
    @route.get("/name", tags=tags, response_model=PlayerInDB)
    async def name(player_name: str) -> PlayerInDB:
        if player := await get_player_by_name(player_name):
            return player
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with name {player_name} not found"
        )

    @staticmethod
    @route.get("/playfab-id", tags=tags, response_model=PlayerInDB)
    async def playfab_id(playfab_id):
        if player := await get_player_by_playfab_id(playfab_id):
            return player
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with playfab id {playfab_id} not found"
        )

    @staticmethod
    @route.get("/discord-id", tags=tags, response_model=PlayerInDB)
    async def discord_id(discord_id: int):
        return await get_player_by_discord_id(discord_id)

    @staticmethod
    @route.post("/create", tags=tags, response_model=BaseSchema)
    async def create(player: Player, auth=Depends(JWTBearer())) -> BaseSchema:
        await check_user(token=auth[0], user_id=auth[-1])
        log.info(f"User id \"{auth[-1]}\" issued a creation of Mordhau Player \"{player.player_name}\"")
        return BaseSchema(
            message="Created player",
            extra=[
                {"player_id": await create_player(player)}
            ]
        )

    @staticmethod
    @route.post("/delete", tags=tags)
    async def delete(player_id: UUID4, auth=Depends(JWTBearer())):
        await check_user(token=auth[0], user_id=auth[-1])
        if player_id and await get_player_by_id(player_id):
            log.info(f"User id \"{auth[-1]}\" issued a delete of Mordhau Player id \"{player_id}\"")
            await delete_player(player_id)
            return {"Deleted player": player_id}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player {player_id} could not be found"
        )

    @staticmethod
    @route.post("/update-discord-id", tags=tags, response_model=BaseSchema)
    async def update_discord_id(player_id: UUID4,
                                # That defines the minimum value for a discord id
                                discord_id: int = Query(..., gt=9999999999999999),
                                auth=Depends((JWTBearer()))):
        await check_user(token=auth[0], user_id=auth[-1])
        if await get_player_by_id(player_id):
            log.info(f"User ID \"{auth[-1]}\" updated player_id \"{player_id}\" discord id to \"{discord_id}")
            await update_player_discord_id(player_id, discord_id)
            return BaseSchema(
                message="Updated discord id for " + str(player_id),
                extra=[{"discord_id": discord_id, "player_id": str(player_id)}]
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player {player_id} could not be found"
        )

    @staticmethod
    @route.post("/update-name", tags=tags, response_model=BaseSchema)
    async def update_name(name: str, player_id: UUID4, auth=Depends(JWTBearer())):
        await check_user(token=auth[0], user_id=auth[-1])
        if await get_player_by_id(player_id):
            log.info(f"User ID \"{auth[-1]}\" updated player_id \"{player_id}\" name to \"{name}\"")
            await update_player_name(player_id, name)
            return BaseSchema(
                message="Updated name for " + str(player_id),
                extra=[{"name": name, "player_id": player_id}]
            )

    @staticmethod
    @route.post("/make-ambassador", tags=tags, response_model=BaseSchema)
    async def make_ambassador(player_id: UUID4, auth=Depends((JWTBearer()))):
        await check_user(token=auth[0], user_id=auth[-1])
        player = await make_ambassador(player_id)
        return BaseSchema(message=f"Made player {player_id} an ambassador of team {player.team_id}.")

    @staticmethod
    @route.post("/remove-ambassador", tags=tags, response_model=BaseSchema)
    async def remove_ambassador(player_id: UUID4, auth=Depends(JWTBearer())):
        await check_user(token=auth[0], user_id=auth[-1])
        player = await remove_ambassador(player_id)
        return BaseSchema(message=f"Removed player {player_id} from the ambassador role on team {player.team_id}")
