import logging
import asyncio

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
    async def startup() -> None:
        for route in BaseApplication.app.routes:
            if isinstance(route, Route):
                log.info(f"Registered route: \"{route.path}\", methods: {route.methods}")

    def serve(self, sockets=None):
        return UvicornServer(config=self.config).serve(sockets=sockets)

    @staticmethod
    def _setup_logging() -> None:
        log_format = "[%(asctime)s][%(threadName)s][%(name)s.%(funcName)s:%(lineno)d][%(levelname)s] %(message)s"

        file_handler = logging.FileHandler(str(root_path) + "/api.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(log_format))

        logging.basicConfig(
            level=logging.DEBUG,
            format=log_format,
        )

        logging.getLogger().addHandler(file_handler)

    @classmethod
    def run(cls, *args, **kwargs) -> None:

        from API.Endpoints import BaseEndpoint

        # Logging Configuration
        cls._setup_logging()

        # FastAPI setup
        BaseEndpoint.find_subclasses()
        BaseEndpoint.load_endpoints()
        # Finished setup, run it
        loop = asyncio.get_event_loop()

        loop.run_until_complete(asyncio.wait([loop.create_task(cls().serve(sockets=kwargs.get("sockets")))]))

        # To define more asynchronous applications to be ran that can be done via
        # loop.create_task(YOUR_APPLICATION) pior to loop.run_until_complete


__all__ = [
    "BaseApplication"
]
