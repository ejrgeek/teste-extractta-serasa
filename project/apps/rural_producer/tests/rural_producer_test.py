from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from faker import Faker
from pycpfcnpj import gen, validate
from apps.rural_producer.models import Farm, RuralProducer
from django.contrib.auth.models import User


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
            created_by=self.user
        )

    def test_create_rural_producer_with_cpf(self):
        payload = {
            "producer_name": self.faker.name(),
            "document_type": "CPF",
            "document": gen.cpf(),
            "farm": self.farm.id,
            "city": self.faker.city(),
            "state": self.faker.state_abbr(),
            "created_by": self.user.id
        }
        response = self.client.post(reverse('ruralproducer-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_rural_producer_with_invalid_cpf(self):
        invalid_cpf = "12345678900"
        payload = {
            "producer_name": self.faker.name(),
            "document_type": "CPF",
            "document": invalid_cpf,
            "farm": self.farm.id,
            "city": self.faker.city(),
            "state": self.faker.state_abbr(),
            "created_by": self.user.id
        }
        response = self.client.post(reverse('ruralproducer-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_rural_producer_with_cnpj(self):
        payload = {
            "producer_name": self.faker.name(),
            "document_type": "CNPJ",
            "document": gen.cnpj(),
            "farm": self.farm.id,
            "city": self.faker.city(),
            "state": self.faker.state_abbr(),
            "created_by": self.user.id
        }
        response = self.client.post(reverse('ruralproducer-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_rural_producer(self):
        rural_producer = RuralProducer.objects.create(
            producer_name=self.faker.name(),
            document_type="CPF",
            document=gen.cpf(),
            farm=self.farm,
            city=self.faker.city(),
            state=self.faker.state_abbr(),
            created_by=self.user
        )
        payload = {
            "producer_name": self.faker.name(),
            "city": "Nova Cidade"
        }
        response = self.client.put(reverse('ruralproducer-update-producer', args=[rural_producer.id]), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['producer_name'], payload['producer_name'])
        self.assertEqual(response.data['city'], payload['city'])

    def test_delete_rural_producer(self):
        rural_producer = RuralProducer.objects.create(
            producer_name=self.faker.name(),
            document_type="CPF",
            document=gen.cpf(),
            farm=self.farm,
            city=self.faker.city(),
            state=self.faker.state_abbr(),
            created_by=self.user
        )
        response = self.client.delete(reverse('ruralproducer-delete-producer', args=[rural_producer.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
