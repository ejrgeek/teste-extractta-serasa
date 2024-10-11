from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.authentication.api.serializers import UserSerializer
from sentry_sdk import capture_exception

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            capture_exception(e)
            return Response(
                {"error": "Erro ao recuperar usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            capture_exception(e)
            return Response(
                {"error": "Erro ao criar usuário."}, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk=None, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            capture_exception(e)
            return Response(
                {"error": "Erro ao atualizar usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            user = self.get_object()
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            capture_exception(e)
            return Response(
                {"error": "Erro ao remover usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )
