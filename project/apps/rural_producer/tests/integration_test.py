# tests/test_integration.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.rural_producer.models import RuralProducer, Farm
from faker import Faker

fake = Faker()


class RuralProducerIntegrationTest(APITestCase):

    def setUp(self):
        self.farm = Farm.objects.create(
            farm_name=fake.company(),
            total_area_hectares=100.0,
            agricultural_area_hectares=50.0,
            vegetation_area_hectares=40.0,
            created_by=fake.uuid4(),
        )
        self.producer_data = {
            "document_type": "CPF",
            "document": "12345678909",
            "producer_name": fake.name(),
            "farm": self.farm.id,
            "city": fake.city(),
            "state": fake.state_abbr(),
            "created_by": fake.uuid4(),
        }
        self.producer = RuralProducer.objects.create(**self.producer_data)

    def test_create_rural_producer(self):
        """Test creating a new rural producer"""
        url = reverse("ruralproducer-list")
        response = self.client.post(url, self.producer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_rural_producer(self):
        """Test updating an existing rural producer"""
        url = reverse("ruralproducer-detail", kwargs={"pk": self.producer.id})
        updated_data = self.producer_data.copy()
        updated_data["producer_name"] = "Updated Name"
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["producer_name"], "Updated Name")

    def test_delete_rural_producer(self):
        """Test deleting a rural producer"""
        url = reverse("ruralproducer-detail", kwargs={"pk": self.producer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RuralProducer.objects.filter(id=self.producer.id).exists())
