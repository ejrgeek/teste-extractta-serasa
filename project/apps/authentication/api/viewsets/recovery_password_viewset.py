import os

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from apps.authentication.api.serializers import (
    ChangePasswordSerializer,
    RecoveryPasswordSerializer,
    EmailRecoveryPasswordSerializer,
)


class ChangePasswordViewSet(viewsets.ViewSet):
    """
    ViewSet para alterar a senha de um usuário autenticado.
    """

    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            if not check_password(old_password, user.password):
                return Response(
                    {"detail": "A senha antiga está incorreta."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"detail": "Senha alterada com sucesso!"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecoveryPasswordViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RecoveryPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get("email")
            new_password = serializer.data.get("new_password")
            user = get_object_or_404(User, email=email)

            # Define a nova senha
            user.set_password(new_password)
            user.save()

            return Response(
                {"detail": "Senha redefinida com sucesso!"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailRecoveryPasswordViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = EmailRecoveryPasswordSerializer(data=request.data)

        EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
        LINK_PARA_REDEFINICAO = os.getenv("LINK_PARA_REDEFINICAO")

        if serializer.is_valid():
            email = serializer.data.get("email")
            user = get_object_or_404(User, email=email)

            send_mail(
                "Recuperação de senha",
                f"Clique no link para recuperar sua senha: {LINK_PARA_REDEFINICAO}",
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return Response(
                {"detail": "E-mail de recuperação enviado!"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
