from django.urls import path
from knox import views as knox_views

from apps.authentication.api.viewsets.login_viewset import LoginUserView

urlpatterns = [
    # login_logout
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", knox_views.LogoutView.as_view(), name="logout"),
]
