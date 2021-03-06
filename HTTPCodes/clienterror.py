from HTTPCodes import Response

_TYPE = "Client Error"


class BadRequest(Response):
    code = 400
    name = "Bad Request"
    type = _TYPE
    message = None


class Unauthorized(Response):
    code = 401
    name = "Unauthorized"
    type = _TYPE
    message = None


class PaymentRequired(Response):
    code = 402
    name = "Payment Required"
    type = _TYPE
    message = None


class Forbidden(Response):
    code = 403
    name = "Forbidden"
    type = _TYPE
    message = None


class NotFound(Response):
    code = 404
    name = "Not Found"
    type = _TYPE
    message = None


class MethodNotAllowed(Response):
    code = 405
    name = "Method Not Allowed"
    type = _TYPE
    message = None


class NotAcceptable(Response):
    code = 406
    name = "Not Acceptable"
    type = _TYPE
    message = None


class ProxyAuthenticationRequired(Response):
    code = 407
    name = "Proxy Authentication Required"
    type = _TYPE
    message = None


class RequestTimeout(Response):
    code = 408
    name = "Request Timeout"
    type = _TYPE
    message = None


class Conflict(Response):
    code = 409
    name = "Conflict"
    type = _TYPE
    message = None


class Gone(Response):
    code = 410
    name = "Gone"
    type = _TYPE
    message = None


class LengthRequired(Response):
    code = 411
    name = "Length Required"
    type = _TYPE
    message = None


class PreconditionFailed(Response):
    code = 412
    name = "Precondition Failed"
    type = _TYPE
    message = None


class PayloadTooLarge(Response):
    code = 413
    name = "Precondition Failed"
    type = _TYPE
    message = None


class URITooLong(Response):
    code = 414
    name = "URI Too Long"
    type = _TYPE
    message = None


class UnsupportedMediaType(Response):
    code = 415
    name = "Unsupported Media Type"
    type = _TYPE
    message = None


class RangeNotSatisfiable(Response):
    code = 416
    name = "Range Not Satisfiable"
    type = _TYPE
    message = None


class ExpectationFailed(Response):
    code = 417
    name = "Expectation Failed"
    type = _TYPE
    message = None


class ImATeapot(Response):
    code = 418
    name = "I'm a teapot"
    type = _TYPE
    message = None


class MisdirectedRequest(Response):
    code = 421
    name = "Misdirected Request"
    type = _TYPE
    message = None


class UnprocessableEntity(Response):
    code = 422
    name = "Unprocessable Entity"
    type = _TYPE
    message = None


class Locked(Response):
    code = 423
    name = "Locked"
    type = _TYPE
    message = None


class FailedDependency(Response):
    code = 424
    name = "Failed Dependency"
    type = _TYPE
    message = None


class TooEarly(Response):
    code = 425
    name = "Too Early"
    type = _TYPE
    message = None


class UpgradeRequired(Response):
    code = 426
    name = "Upgrade Required"
    type = _TYPE
    message = None


class PreconditionRequired(Response):
    code = 428
    name = "Precondition Required"
    type = _TYPE
    message = None


class TooManyRequests(Response):
    code = 429
    name = "Too Many Requests"
    type = _TYPE
    message = None


class RequestHeaderFieldsTooLarge(Response):
    code = 431
    name = "Request Header Fields Too Large"
    type = _TYPE
    message = None


class UnavailableForLegalReasons(Response):
    code = 451
    name = "Unavailable For Legal Reasons"
    type = _TYPE
    message = None
