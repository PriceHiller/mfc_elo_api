from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from API.Endpoints import BaseEndpoint


class Root(BaseEndpoint):
    route = APIRouter()

    @staticmethod
    @route.get("/", tags=["root"])
    async def root():
        return RedirectResponse(url="/docs")
