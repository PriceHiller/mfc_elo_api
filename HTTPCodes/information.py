from HTTPCodes import Response

_TYPE = "Information"


class Continue(Response):
    code = 100
    name = "Continue"
    type = _TYPE
    message = None


class SwitchingProtocol(Response):
    code = 101,
    name = "Switching Protocol",
    type = _TYPE,
    message = None


class Processing(Response):
    code = 102,
    name = "Processing",
    type = _TYPE,
    message = None


class EarlyHints(Response):
    code = 103,
    name = "Early Hint",
    type = _TYPE,
    message = None

