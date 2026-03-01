class ZeptomcError(Exception):
    pass


class AuthenticationError(ZeptomcError):
    pass


class RefreshError(ZeptomcError):
    pass


class ValidationError(ZeptomcError):
    pass
