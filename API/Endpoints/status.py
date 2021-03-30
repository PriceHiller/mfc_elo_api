from fastapi import APIRouter

from API.Endpoints import BaseEndpoint

from API.Schemas import BaseSchema


class Status(BaseEndpoint):
    status = "Online"

    tags = ["status"]

    route = APIRouter()

    @staticmethod
    @route.get("/status", tags=tags)
    async def _status():
        return BaseSchema(message=Status.status)
