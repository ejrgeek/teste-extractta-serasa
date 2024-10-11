from .auth_errors import AuthErrors


class UninformedCredentialsException(Exception):
    message = AuthErrors.UNINFORMED_CREDENTIALS


class InvalidUserCredentials(Exception):
    message = AuthErrors.INVALID_CREDENTIALS


class AccessBlocked(Exception):
    message = AuthErrors.ACCESS_BLOCKED


class NoPermission(Exception):
    message = AuthErrors.NO_PERMISSION
