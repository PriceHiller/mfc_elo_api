from HTTPCodes import Response

_TYPE = "Server Error"


class InternalServerError(Response):
    code = 500
    name = "Internal Server Error"
    type = _TYPE
    message = None


class NotImplemented(Response):
    code = 501
    name = "Not Implemented"
    type = _TYPE
    message = None


class BadGateway(Response):
    code = 502
    name = "Not Implemented"
    type = _TYPE
    message = None


class ServiceUnavailable:
    code = 503
    name = "Service Unavailable"
    type = _TYPE
    message = None


class GatewayTimeout:
    code = 504
    name = "Gateway Timeout"
    type = _TYPE
    message = None


class HTTPVersionNotSupported(Response):
    code = 505
    name = "HTTP Version Not Supported"
    type = _TYPE
    message = None


class VariantAlsoNegotiates(Response):
    code = 506
    name = "Variant Also Negotiates"
    type = _TYPE
    message = None


class InsufficientStorage(Response):
    code = 507
    name = "Insufficient Storage"
    type = _TYPE
    message = None


class LoopDetected(Response):
    code = 508
    name = "Loop Detected"
    type = _TYPE
    message = None


class NotExtended(Response):
    code = 510
    name = "Not Extended"
    type = _TYPE
    message = None


class NetworkAuthenticationRequired(Response):
    code = 511
    name = "Network Authentication Required"
    type = _TYPE
    message = None
