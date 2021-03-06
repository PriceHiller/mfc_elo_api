import asyncio
import logging
import pathlib

from API.Endpoints import BaseEndpoint
from API import BaseApplication
from API import base_dir


def setup_logging():
    log_format = "[%(asctime)s][%(threadName)s][%(name)s.%(funcName)s:%(lineno)d][%(levelname)s] %(message)s"

    file_handler = logging.FileHandler(str(pathlib.Path(base_dir)) + "/api.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
    )

    logging.getLogger().addHandler(file_handler)


def main():
    # Logging Configuration
    setup_logging()

    # FastAPI setup
    BaseEndpoint.find_subclasses()

    Application = BaseApplication()
    BaseEndpoint.find_subclasses()
    BaseEndpoint.load_endpoints()

    # Finished setup, run it
    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.wait([loop.create_task(Application.serve())]))

    # To define more asynchronous applications to be ran that can be done via
    # loop.create_task(YOUR_APPLICATION) pior to loop.run_until_complete


if __name__ == "__main__":
    main()
