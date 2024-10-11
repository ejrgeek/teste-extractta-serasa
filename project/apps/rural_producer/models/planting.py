from django.db import models
from uuid import uuid4


class Planting(models.Model):

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        unique=True,
    )

    planting_name = models.CharField(
        max_length=100,
        verbose_name="Plantio",
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
        return self.planting_name

    class Meta:
        verbose_name = "Plantação"
        verbose_name_plural = "Plantações"
