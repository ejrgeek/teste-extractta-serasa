from django.test import TestCase
from faker import Faker
from uuid import uuid4
from apps.rural_producer.models.farm import Farm
from apps.rural_producer.models.planting import Planting
from apps.rural_producer.models.rural_producer import RuralProducer
from django.contrib.auth import get_user_model

User = get_user_model()
fake = Faker()


class RuralProducerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username=fake.user_name(), email=fake.email(), password="testpassword123"
        )

        self.farm = Farm.objects.create(
            id=uuid4(),
            farm_name=fake.company(),
            total_area_hectares=fake.random_number(digits=3),
            agricultural_area_hectares=fake.random_number(digits=2),
            vegetation_area_hectares=fake.random_number(digits=2),
            created_by=self.user,
        )

    def test_create_rural_producer(self):
        producer = RuralProducer.objects.create(
            id=uuid4(),
            document_type="CPF",
            document=fake.ssn(),
            producer_name=fake.name(),
            farm=self.farm,
            city=fake.city(),
            state=fake.state(),
            created_by=self.user,
        )

        self.assertEqual(RuralProducer.objects.count(), 1)
        self.assertEqual(str(producer), f"{producer.producer_name} - {producer.farm}")
        self.assertEqual(producer.farm.farm_name, self.farm.farm_name)


class PlantingTest(TestCase):

    def test_create_planting(self):
        planting = Planting.objects.create(
            id=uuid4(),
            planting_name=fake.word(),
        )

        self.assertEqual(Planting.objects.count(), 1)
        self.assertEqual(str(planting), planting.planting_name)


class FarmTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username=fake.user_name(), email=fake.email(), password="testpassword123"
        )

        self.planting1 = Planting.objects.create(
            id=uuid4(),
            planting_name=fake.word(),
        )

        self.planting2 = Planting.objects.create(
            id=uuid4(),
            planting_name=fake.word(),
        )

    def test_create_farm(self):
        farm = Farm.objects.create(
            id=uuid4(),
            farm_name=fake.company(),
            total_area_hectares=fake.random_number(digits=3),
            agricultural_area_hectares=fake.random_number(digits=2),
            vegetation_area_hectares=fake.random_number(digits=2),
            created_by=self.user,
        )

        farm.planted_crops.add(self.planting1, self.planting2)

        self.assertEqual(Farm.objects.count(), 1)
        self.assertEqual(str(farm), farm.farm_name)
        self.assertEqual(farm.planted_crops.count(), 2)
