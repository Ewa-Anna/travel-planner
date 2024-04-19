from rest_framework import viewsets

from authx.utils import NoPagination

from .models import Accommodation, Transportation
from .serializers import AccommodationSerializer, TransportationSerializer


class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    pagination_class = NoPagination

    def get_queryset(self):
        queryset = Accommodation.objects.all().order_by("name")
        return queryset


class TransportationViewSet(viewsets.ModelViewSet):
    queryset = Transportation.objects.all()
    serializer_class = TransportationSerializer
    pagination_class = NoPagination

    def get_queryset(self):
        queryset = Transportation.objects.all().order_by("name")
        return queryset
