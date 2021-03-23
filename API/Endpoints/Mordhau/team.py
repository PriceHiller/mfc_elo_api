import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status
from fastapi.exceptions import HTTPException

from API.auth import JWTBearer

from API.Database.crud.Mordhau.team import get_teams
from API.Database.crud.Mordhau.team import get_team_by_id
from API.Database.crud.Mordhau.team import get_team_by_name
from API.Database.crud.Mordhau.team import create_team
from API.Database.crud.Mordhau.team import delete_team
from API.Database.crud.Mordhau.team import update_name
from API.Database.crud.Mordhau.team import update_elo

from API.Endpoints import BaseEndpoint

from API.Schemas.Mordhau.team import Team

log = logging.getLogger(__name__)


class MordhauTeam(BaseEndpoint):
    tags = ["mordhau-team"]

    route = APIRouter(prefix="/team")

    @staticmethod
    @route.get("/all", tags=tags)
    async def team():
        return await get_teams()

    @staticmethod
    @route.get("/id", tags=tags)
    async def _id(id: str) -> [Team]:
        if team := await get_team_by_id(id):
            return team
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id \"{id}\" not found"
        )

    @staticmethod
    @route.get("/name", tags=tags)
    async def name(team_name: str):
        if team := await get_team_by_name(team_name):
            return team
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with name \"{team_name}\" not found"
        )

    @staticmethod
    @route.post("/name", tags=tags)
    async def update_name(new_name: str,
                          team_id: str = Query(..., min_length=32, max_length=36),
                          auth=Depends(JWTBearer())):
        if team_id and await get_team_by_id(team_id):
            log.info(f"User id \"{auth[-1]}\" updated team_id \"{team_id}\" team name to \"{new_name}\"")
            return await update_name(team_id, new_name)

    @staticmethod
    @route.post("/create", tags=tags)
    async def create(team: Team, auth=Depends(JWTBearer())) -> dict[str, str]:
        log.info(f"User id \"{auth[-1]}\" issued a creation of Mordhau Team \"{team.team_name}\"")
        return {"Team ID": await create_team(team)}

    @staticmethod
    @route.post("/delete", tags=tags)
    async def delete(team_id: str = Query(..., min_length=32, max_length=36), auth=Depends(JWTBearer())):
        if team_id and await get_team_by_id(team_id):
            log.info(f"User id \"{auth[-1]}\" issued a delete of Mordhau Team id \"{team_id}\"")
            await delete_team(team_id)

    @staticmethod
    @route.post("/update-elo", tags=tags)
    async def update_elo(new_elo: int,
                         team_id: str = Query(..., min_length=32, max_length=36),
                         auth=Depends(JWTBearer())):
        if team_id and await get_team_by_id(team_id):
            log.info(f"User id \"{auth[-1]}\" updated team_id \"{team_id}\" elo to {new_elo}")
            return await update_elo(team_id, new_elo)
