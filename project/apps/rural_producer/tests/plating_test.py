from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from faker import Faker
from apps.rural_producer.models import Planting
from django.contrib.auth.models import User


class PlantingTests(APITestCase):

    def setUp(self):
        self.faker = Faker()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_create_planting(self):
        payload = {"planting_name": "Soja", "created_by": self.user.id}
        response = self.client.post(reverse("planting-list"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_planting(self):
        planting = Planting.objects.create(planting_name="Milho")
        payload = {"planting_name": "Algodão"}
        response = self.client.put(
            reverse("planting-update-planting", args=[planting.id]), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["planting_name"], payload["planting_name"])

    def test_delete_planting(self):
        planting = Planting.objects.create(planting_name="Café")
        response = self.client.delete(
            reverse("planting-delete-planting", args=[planting.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
