from rest_framework import serializers
from apps.rural_producer.models import Farm
from apps.rural_producer.api.serializers import PlantingSerializer


class FarmSerializer(serializers.ModelSerializer):
    planted_crops = PlantingSerializer(many=True, read_only=True)

    class Meta:
        model = Farm
        fields = [
            "id",
            "farm_name",
            "total_area_hectares",
            "agricultural_area_hectares",
            "vegetation_area_hectares",
            "planted_crops",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        if (
            data["agricultural_area_hectares"] + data["vegetation_area_hectares"]
            > data["total_area_hectares"]
        ):
            raise serializers.ValidationError(
                "A soma da área agricultável e da área de vegetação não pode ser maior que a área total da fazenda."
            )
        return data
