from rest_framework import serializers
from apps.rural_producer.models import Farm


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = "__all__"
