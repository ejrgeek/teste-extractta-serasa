from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import timedelta
import sentry_sdk

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / "data" / "web"


sentry_sdk.init(
    dsn=os.getenv("SENTRY_KEY"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


SECRET_KEY = os.getenv("SECRET_KEY")


DEBUG = bool(int(os.getenv("DEBUG", 0)))


ALLOWED_HOSTS = [
    host.strip() for host in os.getenv("ALLOWED_HOSTS").split(",") if host.strip()
]

INTERNAL_IPS = [
    host.strip() for host in os.getenv("INTERNAL_IPS").split(",") if host.strip()
]

CORS_ALLOWED_ORIGINS = [
    host.strip()
    for host in os.getenv("CORS_ALLOWED_ORIGINS").split(",")
    if host.strip()
]


CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # external apps
    "rest_framework",
    "knox",
    # my apps
    "apps.authentication",
    "apps.rural_producer",
]


REST_KNOX = {
    "SECURE_HASH_ALGORITHM": "cryptography.hazmat.primitives.hashes.SHA512",
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    "TOKEN_TTL": timedelta(days=int(os.getenv("TOKEN_TTL", 31))),
    "USER_SERIALIZER": "knox.serializers.UserSerializer",
    "TOKEN_LIMIT_PER_USER": int(os.getenv("TOKEN_LIMIT_PER_USER")),
    "AUTO_REFRESH": int(os.getenv("AUTO_REFRESH")),
}

X_FRAME_OPTIONS = "SAMEORIGIN"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "knox.auth.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSESS": [
        "rest_framework.persmissions.IsAuthentication",
    ],
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # "corsheaders.middleware.CorsPostCsrfMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "core.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "core.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "authentication.User"


LANGUAGE_CODE = "pt-br"


TIME_ZONE = "America/Fortaleza"


USE_I18N = True


USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = DATA_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = DATA_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
