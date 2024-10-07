from .base import *
from dj_database_url import parse as dburl
from decouple import config


default_dburl = "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")

DATABASES = {
    "default": config("DATABASE_URL", default=default_dburl, cast=dburl),
}
