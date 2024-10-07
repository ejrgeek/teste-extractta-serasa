from django.db import models
from uuid import uuid4

from apps.rural_producer.models import Planting


class Farm(models.Model):

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        unique=True,
    )

    farm_name = models.CharField(
        max_length=255,
        verbose_name="Nome da Fazenda",
    )

    total_area_hectares = models.FloatField()

    agricultural_area_hectares = models.FloatField()

    vegetation_area_hectares = models.FloatField()

    planted_crops = models.ManyToManyField(Planting)

    created_by = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        verbose_name="Criado por",
    )

    created_at = models.DateTimeField(
        auto_created=True,
        auto_now_add=True,
        verbose_name="Criado em",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        auto_created=True,
        verbose_name="Atualizado em",
    )

    def __str__(self):
        return self.farm_name
