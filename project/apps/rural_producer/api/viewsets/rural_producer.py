from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.rural_producer.models.rural_producer import RuralProducer
from apps.rural_producer.api.serializers.rural_producer import RuralProducerSerializer


class RuralProducerViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = RuralProducer.objects.all()
    serializer_class = RuralProducerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        producer_name = self.request.query_params.get("producer_name")
        city = self.request.query_params.get("city")
        state = self.request.query_params.get("state")
        if producer_name:
            queryset = queryset.filter(producer_name__icontains=producer_name)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if state:
            queryset = queryset.filter(state__icontains=state)
        return queryset

    @action(detail=True, methods=["put"], url_path="update-producer")
    def update_producer(self, request, pk=None):
        producer = self.get_object()
        serializer = self.get_serializer(producer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"], url_path="delete-producer")
    def delete_producer(self, request, pk=None):
        producer = self.get_object()
        producer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
