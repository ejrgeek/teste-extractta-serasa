from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from apps.rural_producer.models import Farm, Planting, RuralProducer
from apps.rural_producer.api.serializers import FarmSerializer


class FarmViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        farm_name = self.request.query_params.get("farm_name")
        state = self.request.query_params.get("state")
        if farm_name:
            queryset = queryset.filter(farm_name__icontains=farm_name)
        if state:
            queryset = queryset.filter(ruralproducer__state=state)
        return queryset

    @action(detail=False, methods=["get"], url_path="total-farms")
    def total_farms(self, request):
        total_farms = self.get_queryset().count()
        return Response({"total_farms": total_farms})

    @action(detail=False, methods=["get"], url_path="total-area-hectares")
    def total_area_hectares(self, request):
        total_area = self.get_queryset().aggregate(Sum("total_area_hectares"))[
            "total_area_hectares__sum"
        ]
        return Response({"total_area_hectares": total_area})

    @action(detail=False, methods=["get"], url_path="pie-chart-by-state")
    def pie_chart_by_state(self, request):
        data = (
            RuralProducer.objects.values("state")
            .annotate(total=Count("farm"))
            .order_by("-total")
        )
        return Response({"data": data})

    @action(detail=False, methods=["get"], url_path="pie-chart-by-crop")
    def pie_chart_by_crop(self, request):
        data = (
            Planting.objects.values("planting_name")
            .annotate(total=Count("farm"))
            .order_by("-total")
        )
        return Response({"data": data})

    @action(detail=False, methods=["get"], url_path="pie-chart-by-land-use")
    def pie_chart_by_land_use(self, request):
        total_agricultural_area = self.get_queryset().aggregate(
            Sum("agricultural_area_hectares")
        )["agricultural_area_hectares__sum"]
        total_vegetation_area = self.get_queryset().aggregate(
            Sum("vegetation_area_hectares")
        )["vegetation_area_hectares__sum"]
        return Response(
            {
                "agricultural_area": total_agricultural_area,
                "vegetation_area": total_vegetation_area,
            }
        )
