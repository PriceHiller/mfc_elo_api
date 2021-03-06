from API.Endpoints import BaseEndpoint

from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse


class Test(BaseEndpoint):
    route = APIRouter()

    @staticmethod
    @route.get("/test", response_class=HTMLResponse)
    async def test(request: Request, id: int = 5):
        return Test.template_response("index.html", request=request, id=id)
