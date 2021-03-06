import importlib
import pkgutil

import fastapi
from fastapi import Request

from API import BaseApplication

TemplateResponse = BaseApplication.templates.TemplateResponse


class BaseEndpoint:

    @staticmethod
    def find_subclasses(package: str = "API.Endpoints", recursive: bool = True):
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
    def load_endpoints():
        for subclass in BaseEndpoint.__subclasses__():
            if hasattr(subclass, "route"):
                router: fastapi.APIRouter = getattr(subclass, "route")
                if not isinstance(router, fastapi.APIRouter):
                    raise TypeError(f"\"{subclass.__name__}\" \"route\" attribute is not an \"APIRouter\"")
                BaseApplication.app.include_router(router)
            else:
                raise AttributeError(f"\"{subclass.__name__}\" does not have an attribute \"route\"")

    @staticmethod
    def html_response(filename: str, request: Request, **template_data):
        return TemplateResponse(filename, {"request": request, **template_data})

    @classmethod
    def json_response(cls, message: str = None, data: dict = None, *extra_info, **kwargs):
        name = cls.__name__
        return BaseResponse(name=name, message=message, data=data, *extra_info, **kwargs).response


class BaseResponse:

    def __init__(self,
                 name: str,
                 message: str = None,
                 data: dict = None,
                 *extra_info,
                 **kwargs):
        self.response = {
            "name": name,
            "message": message,
            "data": data,
            **kwargs,
            "extra": [info for info in extra_info]}


__all__ = [
    "BaseEndpoint",
    "BaseResponse"
]
