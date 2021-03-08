from fastapi import APIRouter

from API.Endpoints import BaseEndpoint


class Status(BaseEndpoint):

    status = "Online"

    route = APIRouter()

    @staticmethod
    @route.get("/status")
    async def _status():
        return {"Status": Status.status}
