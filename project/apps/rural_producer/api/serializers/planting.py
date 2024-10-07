from rest_framework import serializers
from apps.rural_producer.models import Planting


class PlantingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planting
        fields = "__all__"
