# tests/test_models.py
from django.core.exceptions import ValidationError
from django.test import TestCase
from apps.rural_producer.models import Farm
from faker import Faker

fake = Faker()

class FarmModelTest(TestCase):
    
    def setUp(self):
        self.farm = Farm.objects.create(
            farm_name=fake.company(),
            total_area_hectares=100.0,
            agricultural_area_hectares=50.0,
            vegetation_area_hectares=40.0,
            created_by=fake.uuid4(),
        )

    def test_valid_farm_areas(self):
        """Test if agricultural_area + vegetation_area <= total_area"""
        self.assertTrue(
            self.farm.agricultural_area_hectares + self.farm.vegetation_area_hectares <= self.farm.total_area_hectares
        )

    def test_invalid_farm_areas(self):
        """Test invalid farm areas where the sum exceeds the total area"""
        self.farm.agricultural_area_hectares = 60.0
        self.farm.vegetation_area_hectares = 50.0  # Exceeds total_area
        with self.assertRaises(ValidationError):
            self.farm.clean()  # Clean will raise validation error
