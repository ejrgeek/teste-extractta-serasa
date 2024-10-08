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

    def test_recovery_password_email_not_found(self):
        response = self.client.post(
            self.password_recovery_url, {"email": faker.email()}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
