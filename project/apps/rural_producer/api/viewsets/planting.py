from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.rural_producer.models.planting import Planting
from apps.rural_producer.api.serializers.planting import PlantingSerializer


class PlantingViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Planting.objects.all()
    serializer_class = PlantingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        planting_name = self.request.query_params.get("planting_name")
        if planting_name:
            queryset = queryset.filter(planting_name__icontains=planting_name)
        return queryset

    @action(detail=True, methods=["put"], url_path="update-planting")
    def update_planting(self, request, pk=None):
        planting = self.get_object()
        serializer = self.get_serializer(planting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"], url_path="delete-planting")
    def delete_planting(self, request, pk=None):
        planting = self.get_object()
        planting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
