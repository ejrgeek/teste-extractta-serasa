from rest_framework import serializers
from apps.rural_producer.models import RuralProducer


class ProdutorRuralSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuralProducer
        fields = "__all__"
