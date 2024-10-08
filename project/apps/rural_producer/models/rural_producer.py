from django.db import models
from uuid import uuid4

from apps.rural_producer.models import Farm


class RuralProducer(models.Model):

    CPF_CNPJ_CHOICES = (
        ("CPF", "CPF"),
        ("CNPJ", "CNPJ"),
    )

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        unique=True,
    )

    document_type = models.CharField(
        max_length=4,
        choices=CPF_CNPJ_CHOICES,
        verbose_name="Tipo do Documento",
    )

    document = models.CharField(
        max_length=20,
        unique=True,
    )

    producer_name = models.CharField(
        max_length=255,
        verbose_name="Nome do Produtor",
    )

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    city = models.CharField(
        max_length=100,
        verbose_name="Cidade",
    )

    state = models.CharField(
        max_length=100,
        verbose_name="Estado",
    )

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
        return f"{self.producer_name} - {self.farm}"

    class Meta:
        verbose_name = "Produtor Rural"
        verbose_name_plural = "Produtores Rurais"
