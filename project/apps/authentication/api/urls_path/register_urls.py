from django.urls import path

from apps.authentication.api.viewsets.register_viewset import RegisterUserViewSet

urlpatterns = [
    # register
    path("register/", RegisterUserViewSet.as_view(), name="register")
]
