from rest_framework import generics
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from knox.models import AuthToken

from sentry_sdk import capture_exception

from apps.authentication.api.errors.auth_errors import AuthErrors

from apps.authentication.api.serializers import RegisterSerializer, UserSerializer


class RegisterUserViewSet(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:

            email = request.data.get("email")
            username = request.data.get("username")

            if (get_user_model().objects.filter(email=email).exists()) or (
                get_user_model().objects.filter(username=username).exists()
            ):
                raise IntegrityError()

            if (
                request.data.get("password") == None
                or len(request.data.get("password")) < 8
            ):
                #! TODO: REMOVE HARD CODE
                return Response(
                    {"message": "A senha não obedece os criterios do sistema"}
                )

            user = get_user_model().objects.create(
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                username=username,
            )

            user.set_password(request.data.get("password"))

            user.save()

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "token": AuthToken.objects.create(user)[1],
                },
                status=status.HTTP_201_CREATED,
            )

        except IntegrityError as e:
            capture_exception(e)
            return Response(
                AuthErrors.CREDENTIAS_ALREADY_IN_USE,
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            capture_exception(e)
            return Response(
                AuthErrors.DEFAULT_ERROR,
                status=status.HTTP_400_BAD_REQUEST,
            )
