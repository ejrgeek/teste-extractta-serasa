from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from faker import Faker
from pycpfcnpj import gen
from apps.rural_producer.models import Farm, RuralProducer, Planting
from django.contrib.auth.models import User


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
