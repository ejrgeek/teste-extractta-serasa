from .base import *


DATABASES = {
    "default": {
        "ENGINE": os.getenv("HOMOL_DB_ENGINE"),
        "NAME": os.getenv("HOMOL_DB_NAME"),
        "USER": os.getenv("HOMOL_DB_USERNAME"),
        "PASSWORD": os.getenv("HOMOL_DB_PASSWORD"),
        "HOST": os.getenv("HOMOL_HOST"),
        "PORT": os.getenv("HOMOL_PORT"),
    }
}
