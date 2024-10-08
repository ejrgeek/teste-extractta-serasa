from pycpfcnpj import cpfcnpj
from rest_framework import serializers
from apps.rural_producer.models import RuralProducer
from apps.rural_producer.api.serializers import FarmSerializer


class RuralProducerSerializer(serializers.ModelSerializer):
    farm = FarmSerializer(read_only=True)

    class Meta:
        model = RuralProducer
        fields = [
            "id",
            "document_type",
            "document",
            "producer_name",
            "farm",
            "city",
            "state",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate_document(self, value):
        if self.instance:
            if not self._validate_document(value):
                raise serializers.ValidationError("Documento inválido.")
        return value

    def _validate_document(self, document):
        return cpfcnpj.validate(document)
