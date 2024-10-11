from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.authentication.api.viewsets.recovery_password_viewset import (
    ChangePasswordViewSet,
    RecoveryPasswordViewSet,
    EmailRecoveryPasswordViewSet,
)

router = DefaultRouter()
router.register(r"change-password", ChangePasswordViewSet, basename="change-password")
router.register(
    r"recovery-password", RecoveryPasswordViewSet, basename="recovery-password"
)
router.register(
    r"email-recovery-password",
    EmailRecoveryPasswordViewSet,
    basename="email-recovery-password",
)

urlpatterns = [
    path("change-password/", ChangePasswordViewSet.as_view(), name="change_password"),
    path(
        "recovery-password/",
        RecoveryPasswordViewSet.as_view(),
        name="recovery_password",
    ),
    path(
        "email-recovery-password/",
        EmailRecoveryPasswordViewSet.as_view(),
        name="email_recovery_password",
    ),
]
