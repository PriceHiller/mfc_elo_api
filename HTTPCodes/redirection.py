from HTTPCodes import Response

_TYPE = "Redirection"


class MultipleChoice(Response):
    code = 300
    name = "Multiple Choice"
    type = _TYPE
    message = None


class MovedPermanently(Response):
    code = 301
    name = "Moved Permanently"
    type = _TYPE
    message = None


class Found(Response):
    code = 302
    name = "Found"
    type = _TYPE
    message = None


class SeeOther(Response):
    code = 303
    name = "See Other"
    type = _TYPE
    message = None


class NotModified(Response):
    code = 304
    name = "Not Modified"
    type = _TYPE
    message = None


class UseProxy(Response):
    """DEPRECATED"""
    code = 305
    name = "Use Proxy"
    type = _TYPE
    message = None


class Unused(Response):
    """DEPRECATED"""
    code = 306
    name = "Unused"
    type = _TYPE
    message = None


class TemporaryRedirect(Response):
    code = 307
    name = "Temporary Redirect"
    type = _TYPE
    message = None


class PermanentRedirect(Response):
    code = 308
    name = "Permanent Redirect"
    type = _TYPE
    message = None
