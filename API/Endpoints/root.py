from fastapi import APIRouter

from API.Endpoints import BaseEndpoint


class Root(BaseEndpoint):
    route = APIRouter()

    @staticmethod
    @route.get("/", tags=["root"])
    async def root():
        return "Welcome to the root page"
