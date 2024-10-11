from django.test import TestCase
from uuid import UUID
from apps.authentication.models import User
from faker import Faker

fake = Faker()


class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password="testpassword123",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

        self.assertEqual(User.objects.count(), 1)

        self.assertIsInstance(user.id, UUID, "O campo 'id' deve ser um UUID.")

        self.assertIsNotNone(
            user.created_at, "O campo 'created_at' deve ser preenchido automaticamente."
        )

        self.assertIsNotNone(
            user.updated_at, "O campo 'updated_at' deve ser preenchido automaticamente."
        )

    def test_updated_at_field(self):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password="testpassword123",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

        old_updated_at = user.updated_at

        user.first_name = "UpdatedName"
        user.save()

        self.assertGreater(
            user.updated_at,
            old_updated_at,
            "O campo 'updated_at' deve ser atualizado após uma mudança no registro.",
        )

    def test_user_str_method(self):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password="testpassword123",
            first_name="João",
            last_name="Silva",
        )

        expected_str = f"<User: name=João {user.last_login}>"
        self.assertEqual(
            str(user),
            expected_str,
            "O método __str__ deve retornar o nome e o último login do usuário.",
        )
