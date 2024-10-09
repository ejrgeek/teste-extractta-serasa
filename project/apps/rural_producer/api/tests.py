# tests/test_integration.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.rural_producer.models.farm import Farm
from apps.rural_producer.models.planting import Planting
from apps.rural_producer.models.rural_producer import RuralProducer
from faker import Faker

from apps.authentication.models.user import User
from pycpfcnpj import gen

fake = Faker()


class RuralProducerTests(APITestCase):

    def setUp(self):
        self.faker = Faker()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.farm = Farm.objects.create(
            farm_name=self.faker.company(),
            total_area_hectares=200,
            agricultural_area_hectares=150,
            vegetation_area_hectares=50,
            created_by=self.user,
        )

    def test_update_rural_producer(self):
        rural_producer = RuralProducer.objects.create(
            producer_name=self.faker.name(),
            document_type="CPF",
            document=gen.cpf(),
            farm=self.farm,
            city=self.faker.city(),
            state=self.faker.state_abbr(),
            created_by=self.user,
        )
        payload = {"producer_name": self.faker.name(), "city": "Nova Cidade"}
        response = self.client.put(
            reverse("ruralproducer-update-producer", args=[rural_producer.id]), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["producer_name"], payload["producer_name"])
        self.assertEqual(response.data["city"], payload["city"])


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


class FarmTests(APITestCase):

    def setUp(self):
        self.faker = Faker()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_create_farm(self):
        planting = Planting.objects.create(planting_name="Soja")
        payload = {
            "farm_name": self.faker.company(),
            "total_area_hectares": 100,
            "agricultural_area_hectares": 70,
            "vegetation_area_hectares": 30,
            "planted_crops": [planting.id],
            "created_by": self.user.id,
        }
        response = self.client.post(reverse("farm-list"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_farm_total_count(self):
        Farm.objects.create(
            farm_name=self.faker.company(),
            total_area_hectares=150,
            agricultural_area_hectares=90,
            vegetation_area_hectares=60,
            created_by=self.user,
        )
        response = self.client.get(reverse("farm-total-farms"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_farms"], 1)

    def test_farm_total_area(self):
        Farm.objects.create(
            farm_name=self.faker.company(),
            total_area_hectares=200,
            agricultural_area_hectares=150,
            vegetation_area_hectares=50,
            created_by=self.user,
        )
        response = self.client.get(reverse("farm-total-area-hectares"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_area_hectares"], 200)

    def test_pie_chart_by_state(self):
        farm = Farm.objects.create(
            farm_name=self.faker.company(),
            total_area_hectares=100,
            agricultural_area_hectares=70,
            vegetation_area_hectares=30,
            created_by=self.user,
        )
        RuralProducer.objects.create(
            producer_name=self.faker.name(),
            document_type="CPF",
            document=gen.cpf(),
            farm=farm,
            city=self.faker.city(),
            state="SP",
            created_by=self.user,
        )
        response = self.client.get(reverse("farm-pie-chart-by-state"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["data"]), 1)
