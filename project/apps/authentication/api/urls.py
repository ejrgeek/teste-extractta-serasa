from django.urls import path, include

from apps.authentication.api.urls_path import login_urls, register_urls, user_urls

urlpatterns = [
    # auth
    path("auth/", include(login_urls), name="login"),
    path("auth/", include(register_urls), name="logout"),
    path("auth/", include(user_urls), name="user"),
]
