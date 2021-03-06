from HTTPCodes import Response

_TYPE = "Success"


class OK(Response):
    code = 200
    name = "OK"
    type = _TYPE
    message = None


class Created(Response):
    code = 201
    name = "Created"
    type = _TYPE
    message = None


class Accepted(Response):
    code = 202,
    name = "Accepted"
    type = _TYPE
    message = None


class NonAuthoritativeInformation(Response):
    code = 203
    name = "Non-Authoritative Information"
    type = _TYPE
    message = None


class NoContent(Response):
    code = 204
    name = "No Content"
    type = _TYPE
    message = None


class ResetContent(Response):
    code = 205
    name = "Reset Content"
    type = _TYPE
    message = None


class PartialContent(Response):
    code = 206
    name = "Partial Content"
    type = _TYPE
    message = None


class MultiStatus(Response):
    code = 207
    name = "Mutli-Status"
    type = _TYPE
    message = None


class AlreadyReported(Response):
    code = 208
    name = "Already Reported"
    type = _TYPE
    message = None


class IMUsed(Response):
    code = 226
    name = "IM Used"
    type = _TYPE
    message = None
