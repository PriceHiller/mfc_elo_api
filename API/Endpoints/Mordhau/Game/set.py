import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from fastapi.exceptions import HTTPException

from pydantic import UUID4

from API.Auth import JWTBearer

from API.Database.Crud.Mordhau.Game.set import get_set_by_id
from API.Database.Crud.Mordhau.Game.set import get_sets_by_match_id
from API.Database.Crud.Mordhau.Game.set import get_sets_by_map
from API.Database.Crud.Mordhau.Game.set import get_sets
from API.Database.Crud.Mordhau.Game.set import create_set
from API.Database.Crud.User.user import check_user

from API.Schemas import BaseSchema
from API.Schemas.Mordhau.Game.set import SetInDB
from API.Schemas.Mordhau.Game.set import Set as SchemaSet

from API.Endpoints import BaseEndpoint

log = logging.getLogger(__name__)


class Set(BaseEndpoint):
    tags = ["mordhau-set"]

    route = APIRouter(prefix="/set")

    @staticmethod
    @route.get("/id", tags=tags, response_model=SetInDB)
    async def _id(id: UUID4):
        if set := await get_set_by_id(id):
            return set
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set with id {id} not found"
        )

    @staticmethod
    @route.get("/by-match-id", tags=tags, response_model=list[SetInDB])
    async def get_sets_by_match_id(match_id: UUID4):
        return get_sets_by_match_id(match_id)

    @staticmethod
    @route.get("/by-map", tags=tags, response_model=list[SetInDB])
    async def get_sets_by_map(map_name: str):
        return get_sets_by_map(map_name)

    @staticmethod
    @route.get("/all", tags=tags, response_model=list[SetInDB])
    async def get_all_sets():
        return await get_sets()

    @staticmethod
    @route.post("/create-set", tags=tags, response_model=BaseSchema)
    async def create_set(map_name: str, match_id: UUID4, auth=Depends(JWTBearer())):
        await check_user(token=auth[0], user_id=auth[-1])
        set_id = await create_set(SchemaSet(match_id=match_id, map=map_name))
        log.info(f"User \"{auth[-1]}\" created a set \"{set_id}\" under match \"{match_id}\"")
        return BaseSchema(
            message=f"Created a set {set_id} under match {match_id}",
            extra=[
                {
                    "set id": set_id
                }
            ]
        )
