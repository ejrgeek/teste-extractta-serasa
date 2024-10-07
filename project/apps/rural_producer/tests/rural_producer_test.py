# tests/test_models.py
from django.test import TestCase
from apps.rural_producer.models import RuralProducer, Farm
from django.core.exceptions import ValidationError
from faker import Faker

fake = Faker()

class RuralProducerModelTest(TestCase):

    def setUp(self):
        self.farm = Farm.objects.create(
            farm_name=fake.company(),
            total_area_hectares=100.0,
            agricultural_area_hectares=50.0,
            vegetation_area_hectares=40.0,
            created_by=fake.uuid4(),
        )

    def test_valid_cpf(self):
        """Test valid CPF"""
        producer = RuralProducer(
            document_type="CPF",
            document="12345678909",
            producer_name=fake.name(),
            farm=self.farm,
            city=fake.city(),
            state=fake.state_abbr(),
            created_by=fake.uuid4(),
        )
        producer.clean()
        self.assertIsNone(producer.full_clean())

    def test_invalid_cpf(self):
        """Test invalid CPF"""
        producer = RuralProducer(
            document_type="CPF",
            document="12345678900",
            producer_name=fake.name(),
            farm=self.farm,
            city=fake.city(),
            state=fake.state_abbr(),
            created_by=fake.uuid4(),
        )
        with self.assertRaises(ValidationError):
            producer.full_clean()

    def test_valid_cnpj(self):
        """Test valid CNPJ"""
        producer = RuralProducer(
            document_type="CNPJ",
            document="12345678000195",
            producer_name=fake.company(),
            farm=self.farm,
            city=fake.city(),
            state=fake.state_abbr(),
            created_by=fake.uuid4(),
        )
        producer.clean()
        self.assertIsNone(producer.full_clean())

    def test_invalid_cnpj(self):
        """Test invalid CNPJ"""
        producer = RuralProducer(
            document_type="CNPJ",
            document="12345678000199",
            producer_name=fake.company(),
            farm=self.farm,
            city=fake.city(),
            state=fake.state_abbr(),
            created_by=fake.uuid4(),
        )
        with self.assertRaises(ValidationError):
            producer.full_clean()
