import importlib
import logging
import pkgutil

import fastapi
from fastapi import Request

from API import BaseApplication

TemplateResponse = BaseApplication.templates.TemplateResponse

log = logging.getLogger(__name__)


class BaseEndpoint:

    @staticmethod
    def find_subclasses(package: str = "API.Endpoints", recursive: bool = True) -> None:
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
                BaseEndpoint.find_subclasses(full_name, recursive)

    @staticmethod
    def load_endpoints() -> None:
        for subclass in BaseEndpoint.__subclasses__():
            base_subcls_msg = f"The class: \"{subclass.__name__}\" ({subclass.__module__})"
            try:
                router: fastapi.APIRouter = getattr(subclass, "route")
                if not isinstance(router, fastapi.APIRouter):
                    raise TypeError(f"{base_subcls_msg} \"route\" attribute is not a \"fastapi.APIRouter\"")
                BaseApplication.app.include_router(router)
            except AttributeError:
                raise AttributeError(f"{base_subcls_msg} does not have an attribute \"route\"")
            
            
            try:
                tag = getattr(subclass, "tags")
                if len(tag) <= 0:
                    log.warning(f"{base_subcls_msg} tags attribute lacks tag data")
                if not isinstance(tag, list):
                    log.warning(f"{base_subcls_msg} is not of type \"list\"")
            except AttributeError:
                log.warning(f"{base_subcls_msg} lacks a tags list attribute!")

    @staticmethod
    def html_response(filename: str, request: Request, **template_data) -> TemplateResponse:
        return TemplateResponse(filename, {"request": request, **template_data})


__all__ = [
    "BaseEndpoint",
]
