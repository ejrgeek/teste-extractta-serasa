from django.urls import path
from apps.rural_producer.api.views import RuralProducerDetail, RuralProducerListCreate

urlpatterns = [
    path('produtores/', RuralProducerListCreate.as_view(), name='produtor-list-create'),
    path('produtores/<int:pk>/', RuralProducerDetail.as_view(), name='produtor-detail'),
]