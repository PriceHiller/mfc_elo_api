import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from fastapi.exceptions import HTTPException

from pydantic import UUID4

from API.Auth import JWTBearer

from API.Database.Crud.Mordhau.Game.match import get_match_by_id
from API.Database.Crud.Mordhau.Game.match import get_matches_by_team_ids
from API.Database.Crud.Mordhau.Game.match import get_matches_by_team_id
from API.Database.Crud.Mordhau.Game.match import get_matches
from API.Database.Crud.Mordhau.Game.match import create_match

from API.Schemas import BaseSchema
from API.Schemas.Mordhau.Game.match import MatchInDB
from API.Schemas.Mordhau.Game.match import CreateMatch

from API.Endpoints import BaseEndpoint

log = logging.getLogger(__name__)


class Match(BaseEndpoint):
    tags = ["mordhau-match"]

    route = APIRouter(prefix="/match")

    @staticmethod
    @route.get("/id", tags=tags, response_model=MatchInDB)
    async def _id(id: UUID4):
        if match := await get_match_by_id(id):
            return match
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {id} not found"
        )

    @staticmethod
    @route.get("/get-matches-by-teams", tags=tags, response_model=list[MatchInDB])
    async def get_matches_by_team_ids(team1_id, team2_id):
        return get_matches_by_team_ids(team1_id, team2_id)

    @staticmethod
    @route.get("/get-matches-by-team-id", tags=tags, response_model=list[MatchInDB])
    async def get_matches_by_team_id(team_id):
        return get_matches_by_team_id(team_id)

    @staticmethod
    @route.get("/all", tags=tags, response_model=list[MatchInDB])
    async def get_all_matches():
        matches = await get_matches()
        return matches

    @staticmethod
    @route.post("/create-match", tags=tags, response_model=BaseSchema)
    async def create_match(match: CreateMatch, auth=Depends(JWTBearer())):
        match_id = await create_match(match)
        log.info(f"User \"{auth[-1]}\" created a match \"{match_id}\"")
        return BaseSchema(
            message=f"Created match with id: {match_id}",
            extra=[{"match id": match_id}]
        )
