import asyncio
import os

import uvloop
import logging

import importlib
import pkgutil

import fastapi

from distutils.util import strtobool

from starlette.config import Config

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import ORJSONResponse

from starlette.routing import Route

from pathlib import Path

from API.Server import UvicornServer
from API.Server import UvicornConfiguration

log = logging.getLogger(__name__)

root_path = Path(__file__).parent

config = Config(root_path / ".env", environ=os.environ)


class BaseApplication:
    app = fastapi.FastAPI(title="MFC Elo", default_response_class=ORJSONResponse)

    app.mount("/Static", StaticFiles(directory=str(root_path) + "/Static"), name="Static")

    templates = Jinja2Templates(directory=str(root_path) + "/Templates")

    def __init__(
            self,
            uvicorn_config=UvicornConfiguration(
                app=app,
                reload=True,
                loop="uvloop",
            )
    ):
        self.uvicorn_config = uvicorn_config

    @staticmethod
    @app.on_event("startup")
    async def startup() -> None:
        for route in BaseApplication.app.routes:
            if isinstance(route, Route):
                log.info(f"Registered route: \"{route.path}\", methods: {route.methods}")

        from API.Database import BaseDB

        await BaseDB.db.connect()

        BaseDB.create_tables()

    @staticmethod
    @app.on_event("shutdown")
    async def shutdown() -> None:

        from API.Database import BaseDB

        await BaseDB.db.disconnect()

    def serve(self, sockets=None):
        return UvicornServer(config=self.uvicorn_config).serve(sockets=sockets)

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
        from API.Database import BaseDB
        from API.Database.Models import ModelBase

        # Logging Configuration
        cls._setup_logging()

        # FastAPI setup
        BaseEndpoint.load_endpoints()
        ModelBase.load_models()

        instance_config = dynamic_env_load(cls().uvicorn_config, "uvicorn_", UvicornConfiguration)

        instance_config["loop"] = "uvloop"


        # Finished setup, run it
        uvloop.install()
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        loop = asyncio.new_event_loop()

        loop.run_until_complete(asyncio.wait(
            [loop.create_task(cls(UvicornConfiguration(**instance_config)).serve(sockets=kwargs.get("sockets")))]))

        # To define more asynchronous applications to be ran that can be done via
        # loop.create_task(YOUR_APPLICATION) pior to loop.run_until_complete


def find_subclasses(package: str = "API", recursive: bool = True) -> None:
    """ Import all submodules of a module, recursively, including subpackages

    Credit to: https://stackoverflow.com/a/25562415/13079078, Mr. B on stackoverflow
    :param recursive: bool
    :param package: package (name or actual module)
    :type package: str | module
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        importlib.import_module(full_name)
        if recursive and is_pkg:
            find_subclasses(full_name, recursive)


def dynamic_env_load(instance: object, base_match: str, uninstantiated_object) -> dict:
    """
    Will load environment variables based on the arguments that are passed to an object.
    The arguments are found via instance_vars which should be passed in via vars(object()).
    """

    instance_vars = vars(instance)
    for var in dict(instance_vars).keys():
        if env_var := config.get(base_match + var, default=None):
            try:
                instance_vars[var] = strtobool(str(env_var).casefold())
                continue
            except ValueError:
                pass
            if str(env_var).isnumeric():
                instance_vars[var] = int(env_var)
            elif str(env_var).casefold() == "none":
                instance_vars[var] = None
            elif "[" in str(env_var)[0] and "]" in str(env_var)[-1]:
                instance_vars[var] = str(env_var).strip("[").strip("]").split(",")
            else:
                instance_vars[var] = str(env_var)
        try:
            uninstantiated_object(**instance_vars)
        except TypeError as error:
            error_attr = str(error).split(" ")[-1].strip("'")
            instance_vars.pop(error_attr)

    return instance_vars


__all__ = [
    "BaseApplication",
    "find_subclasses"
]
