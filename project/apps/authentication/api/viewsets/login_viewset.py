from django.contrib.auth import login, authenticate, get_user_model

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from knox.views import LoginView as KnoxLoginView
from sentry_sdk import capture_exception

from apps.authentication.api.errors.auth_exception import (
    AccessBlocked,
    InvalidUserCredentials,
    UninformedCredentialsException,
)

from apps.authentication.api.serializers import LoginEmailSerializer


class LoginUserView(KnoxLoginView):
    serializer_class = LoginEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            data = request.data

            if data.get("password") == None or data.get("email") == None:
                raise UninformedCredentialsException

            user = get_user_model().objects.filter(email=data.get("email")).first()

            if user is None or not user.check_password(data.get("password")):
                raise InvalidUserCredentials

            user = authenticate(
                request, username=user.username, password=data.get("password")
            )

            if not user.is_active:
                raise AccessBlocked

            login(request, user)

            return super(LoginUserView, self).post(request, format=None)

        except (
            UninformedCredentialsException,
            InvalidUserCredentials,
            AccessBlocked,
        ) as e:
            capture_exception(e)
            return Response(
                e.message,
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            capture_exception(e)
            return Response(
                e.message,
                status=status.HTTP_400_BAD_REQUEST,
            )
