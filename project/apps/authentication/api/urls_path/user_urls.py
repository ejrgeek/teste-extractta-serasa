from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.authentication.api.viewsets.user_viewset import UserViewSet

urlpatterns = [
    path("user/", UserViewSet.as_view(), name="user"),
]
