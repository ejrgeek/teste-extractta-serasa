# views.py

from rest_framework import generics
from apps.rural_producer.models import RuralProducer
from apps.rural_producer.api.serializers import RuralProducerSerializer

class RuralProducerListCreate(generics.ListCreateAPIView):
    queryset = RuralProducer.objects.all()
    serializer_class = RuralProducerSerializer

class RuralProducerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RuralProducer.objects.all()
    serializer_class = RuralProducerSerializer
