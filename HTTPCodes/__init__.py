class Response:

    @classmethod
    def as_dict(cls):
        variables = list(vars(cls))[-5:-1]
        attrs = {}
        for var in variables:
            value = getattr(cls, str(var))
            if type(value) is tuple:
                value = value[0]
            attrs |= {str(var): value}
        return attrs


__all__ = [
    "Response",
    "information",
    "redirection",
    "success",
    "clienterror",
    "servererror"
]
