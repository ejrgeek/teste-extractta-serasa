from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from faker import Faker
from unittest.mock import patch

# Setup do faker
faker = Faker()


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.password = faker.password(length=12)
        self.user = self.user_model.objects.create_user(
            username=faker.user_name(),
            email=faker.email(),
            password=self.password,
            is_active=True,
        )

        self.login_url = "/api/auth/login/"
        self.logout_url = "/api/auth/logout/"
        self.register_url = "/api/auth/register/"
        self.password_recovery_url = "/api/auth/email-recovery-password/"
        self.recovery_password_url = "/api/auth/recovery-password/"
        self.change_password_url = "/api/auth/change-password/"
        self.new_password = faker.password(length=12)

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {
                "email": self.user.email,
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("expiry", response.data)
        self.assertIn("token", response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            {
                "email": self.user.email,
                "password": "senha_invalida",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Credenciais inválidas.")

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post(
            self.login_url,
            {
                "email": self.user.email,
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Acesso bloqueado.")

    def test_register_success(self):
        user_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "username": faker.user_name(),
            "email": faker.email(),
            "password": faker.password(length=12),
        }
        response = self.client.post(self.register_url, user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertIn("token", response.data)

    def test_register_existing_email(self):
        user_data = {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "username": self.user.username,
            "email": self.user.email,
            "password": self.password,
        }
        response = self.client.post(self.register_url, user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Email já está em uso.")

    def test_recovery_password_email_success(self):
        response = self.client.post(
            self.password_recovery_url, {"email": self.user.email}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "E-mail de recuperação enviado!")

    @patch("sentry_sdk.capture_exception")
    def test_recovery_password_email_not_found(self, mock_capture):
        response = self.client.post(
            self.password_recovery_url, {"email": faker.email()}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_capture.assert_called_once()
        self.assertEqual(response.data, "Usuário não encontrado.")

    def test_change_password_success(self):
        response_login = self.client.post(
            self.login_url,
            {
                "email": self.user.email,
                "password": self.password,
            },
            format="json",
        )

        token = response_login.data["token"]

        response = self.client.post(
            self.change_password_url,
            {
                "old_password": self.password,
                "new_password": self.new_password,
            },
            format="json",
            HTTP_AUTHORIZATION=f"Token {token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Senha alterada com sucesso!")

    def test_change_password_incorrect_old_password(self):
        response_login = self.client.post(
            self.login_url,
            {
                "email": self.user.email,
                "password": self.password,
            },
            format="json",
        )

        token = response_login.data["token"]

        response = self.client.post(
            self.change_password_url,
            {
                "old_password": "senha_incorreta",
                "new_password": self.new_password,
            },
            format="json",
            HTTP_AUTHORIZATION=f"Token {token}",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "A senha antiga está incorreta.")
