import logging

from fastapi import APIRouter
from fastapi import status

from fastapi.exceptions import HTTPException

from API.Auth import JWTBearer

from API.Endpoints import BaseEndpoint


class Match(BaseEndpoint):
    tags = ["mordhau-game"]

    route = APIRouter(prefix="/match")

    @staticmethod
    @route.get("/id", tags=tags)
    async def _id(id: str):
        if match := await get_match_by_id(id):
            return match
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {id} not found"
        )

    # @staticmethod
    # @route.get("/")