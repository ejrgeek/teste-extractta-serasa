from django.test import TestCase
from apps.rural_producer.models import Farm, RuralProducer, Planting
from django.core.exceptions import ValidationError
from pycpfcnpj import cpfcnpj
from pycpfcnpj import gen
from uuid import uuid4

class RuralProducerTestCase(TestCase):

    def setUp(self):
        # Setup de objetos para os testes
        self.farm = Farm.objects.create(
            farm_name="Fazenda Modelo",
            total_area_hectares=100,
            agricultural_area_hectares=70,
            vegetation_area_hectares=30,
        )
        
        self.planting = Planting.objects.create(
            planting_name="Soja",
        )
        
        self.valid_cpf = gen.cpf()
        self.invalid_cpf = "12345678901"

    def test_create_rural_producer_with_valid_cpf(self):
        producer = RuralProducer.objects.create(
            document_type="CPF",
            producer_name="José da Silva",
            farm=self.farm,
            city="Cidade Exemplo",
            state="SP",
            created_by=self.user,  # Assumindo que a lógica de usuário está implementada
        )
        self.assertTrue(cpfcnpj.validate(producer.document_type))

    def test_create_rural_producer_with_invalid_cpf(self):
        with self.assertRaises(ValidationError):
            RuralProducer.objects.create(
                document_type=self.invalid_cpf,
                producer_name="José da Silva",
                farm=self.farm,
                city="Cidade Exemplo",
                state="SP",
                created_by=self.user,
            )

    def test_create_rural_producer_with_valid_cnpj(self):
        valid_cnpj = CNPJ.generate()
        producer = RuralProducer.objects.create(
            document_type="CNPJ",
            producer_name="Fazenda Exemplo",
            farm=self.farm,
            city="Cidade Exemplo",
            state="SP",
            created_by=self.user,
        )
        self.assertTrue(CNPJ().validate(producer.document_type))

    def test_create_rural_producer_with_invalid_cnpj(self):
        with self.assertRaises(ValidationError):
            RuralProducer.objects.create(
                document_type="12345678000100",
                producer_name="Fazenda Exemplo",
                farm=self.farm,
                city="Cidade Exemplo",
                state="SP",
                created_by=self.user,
            )

    def test_areas_should_not_exceed_total_area(self):
        # Tentando criar uma fazenda onde a soma das áreas excede o total
        with self.assertRaises(ValidationError):
            farm = Farm.objects.create(
                farm_name="Fazenda Inválida",
                total_area_hectares=100,
                agricultural_area_hectares=80,
                vegetation_area_hectares=30,  # Excede o total
            )
            farm.clean()  # Validação é executada aqui

    def test_planted_crops_can_have_multiple(self):
        farm = Farm.objects.create(
            farm_name="Fazenda Plural",
            total_area_hectares=150,
            agricultural_area_hectares=100,
            vegetation_area_hectares=50,
        )
        planting1 = Planting.objects.create(planting_name="Soja")
        planting2 = Planting.objects.create(planting_name="Milho")

        farm.planted_crops.add(planting1, planting2)
        farm.save()

        self.assertEqual(farm.planted_crops.count(), 2)
