import os
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAuthenticated, AllowAny


# OPENAPI SETTINGS
# SWAGGER
scheme_view = get_schema_view(
    openapi.Info(
        title="Teste - Brain Agriculture",
        default_version=os.getenv("VERSION"),
        description="Mapeamento de Rotas da API.",
    ),
    public=bool(int(os.getenv("DEBUG"))),
    permission_classes=(AllowAny if os.getenv("ENV") == "DEV" else IsAuthenticated,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
]


if int(os.getenv("DEBUG")):
    urlpatterns += [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            scheme_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "docs/",
            scheme_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc",
            scheme_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]


if os.getenv("ENV") == "dev":
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
