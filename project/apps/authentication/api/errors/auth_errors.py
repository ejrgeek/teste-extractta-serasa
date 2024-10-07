class AuthErrors:
    # code: 10 - 19

    DEFAULT_ERROR = {"code": 0, "message": "Error"}

    CREDENTIAS_ALREADY_IN_USE = {
        "code": 10,
        "message": "Credentials already in use",
    }

    UNINFORMED_CREDENTIALS = {
        "code": 11,
        "message": "Uninformed Credentials",
    }

    INVALID_CREDENTIALS = {
        "code": 12,
        "message": "Invalid Credentials",
    }

    ACCESS_BLOCKED = {
        "code": 13,
        "message": "Access Blocked",
    }

    NO_PERMISSION = {
        "code": 14,
        "message": "No Permission",
    }
