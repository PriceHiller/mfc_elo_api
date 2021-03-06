import logging

import fastapi

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.routing import Route

from pathlib import Path

from API.Server import UvicornServer
from API.Server import UvicornConfiguration

log = logging.getLogger(__name__)

root_path = Path(__file__).parent


class BaseApplication:
    app = fastapi.FastAPI()

    app.mount("/Static", StaticFiles(directory=str(root_path) + "/Static"), name="Static")

    templates = Jinja2Templates(directory=str(root_path) + "/Templates")

    def __init__(self, config: UvicornConfiguration = UvicornConfiguration(app=app)):
        self.config = config

    @staticmethod
    @app.on_event("startup")
    async def startup():
        for route in BaseApplication.app.routes:
            if isinstance(route, Route):
                log.info(f"Registered route: \"{route.path}\", methods: {route.methods}")

    def serve(self, sockets=None):
        return UvicornServer(config=self.config).serve(sockets=sockets)


__all__ = [
    "BaseApplication",
]
