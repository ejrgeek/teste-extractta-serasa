from django.contrib import admin
from apps.rural_producer.models.rural_producer import RuralProducer
from apps.rural_producer.models.farm import Farm
from apps.rural_producer.models.planting import Planting


@admin.register(RuralProducer)
class RuralProducerAdmin(admin.ModelAdmin):
    list_display = (
        "producer_name",
        "document_type",
        "document",
        "farm",
        "city",
        "state",
        "created_at",
    )
    search_fields = (
        "producer_name",
        "document",
        "city",
        "state",
    )
    list_filter = (
        "document_type",
        "state",
        "farm",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = ("producer_name",)


@admin.register(Planting)
class PlantingAdmin(admin.ModelAdmin):
    list_display = (
        "planting_name",
        "created_at",
    )
    search_fields = ("planting_name",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = ("planting_name",)


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = (
        "farm_name",
        "total_area_hectares",
        "agricultural_area_hectares",
        "vegetation_area_hectares",
        "created_at",
    )
    search_fields = ("farm_name",)
    list_filter = ("created_by",)
    filter_horizontal = ("planted_crops",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = ("farm_name",)
