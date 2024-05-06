from django.db.models import Q

from rest_framework import viewsets

from authx.utils import NoPagination

from .models import Accommodation, Transportation
from .serializers import AccommodationSerializer, TransportationSerializer


class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    pagination_class = NoPagination

    def get_queryset(self):
        queryset = Accommodation.objects.filter(created_by=self.request.user).order_by(
            "name"
        )
        query_param = self.request.query_params.get("query")

        if query_param:
            queryset = queryset.filter(Q(name__icontains=query_param))

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TransportationViewSet(viewsets.ModelViewSet):
    queryset = Transportation.objects.all()
    serializer_class = TransportationSerializer
    pagination_class = NoPagination

    def get_queryset(self):
        queryset = Transportation.objects.filter(created_by=self.request.user).order_by(
            "name"
        )
        query_param = self.request.query_params.get("query")

        if query_param:
            queryset = queryset.filter(Q(name__icontains=query_param))

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
