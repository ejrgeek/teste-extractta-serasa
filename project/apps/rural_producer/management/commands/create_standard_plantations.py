from django.core.management.base import BaseCommand
from uuid import uuid4

from apps.rural_producer.models import Planting


class Command(BaseCommand):
    help = "Criação de Plantações Padrões para Preencher o Banco de Dados"

    def handle(self, *args, **kwargs):
        plant_names = ["Soja", "Milho", "Algodão", "Café", "Cana de Açúcar"]

        for name in plant_names:
            Planting.objects.get_or_create(planting_name=name)

        self.stdout.write(self.style.SUCCESS(f"Plantações criadas com sucesso!"))
