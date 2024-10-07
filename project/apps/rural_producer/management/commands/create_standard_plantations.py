# authentication/management/commands/create_user.py

from django.core.management.base import BaseCommand
import random
from uuid import uuid4

from apps.rural_producer.models import Planting


class Command(BaseCommand):
    help = "Criação de Plantações Padrões para Preencher o Banco de Dados"

    def handle(self, *args, **kwargs):

        soybeans = Planting.objects.create(
            planting_name="Soja",
        )
        corn = Planting.objects.create(
            planting_name="Milho",
        )
        cotton = Planting.objects.create(
            planting_name="Algodão",
        )
        coffee = Planting.objects.create(
            planting_name="Café",
        )
        sugar_cane = Planting.objects.create(
            planting_name="Cana de Açucar",
        )

        Planting.objects.bulk_create([soybeans, corn, cotton, coffee, sugar_cane])

        self.stdout.write(self.style.SUCCESS(f"Plantios criados com sucesso!"))
