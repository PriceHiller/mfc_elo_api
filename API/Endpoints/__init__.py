import logging

import fastapi
from fastapi import Request
from fastapi.responses import ORJSONResponse

from API import BaseApplication
from API import find_subclasses

TemplateResponse = BaseApplication.templates.TemplateResponse

log = logging.getLogger(__name__)


class CommonTags:
    jwt = "jwt"
    cookie = "cookie"
    session = "session"
    auth_required = "authentication required"


class BaseEndpoint:

    @staticmethod
    def load_endpoints() -> None:
        find_subclasses("API.Endpoints")
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
    "ORJSONResponse"
]
