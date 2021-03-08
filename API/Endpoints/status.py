from fastapi import APIRouter
from fastapi.responses import UJSONResponse


from API.Endpoints import BaseEndpoint



class Status(BaseEndpoint):

    status = "Online"

    route = APIRouter()

    @staticmethod
    @route.get("/status", response_class=UJSONResponse)
    async def _status():
        return {"Status": Status.status}
