from django.db.models import Q

from rest_framework import viewsets

from authx.utils import NoPagination

from .models import Country, City, POI
from .serializers import CountrySerializer, CitySerializer, POISerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = NoPagination

    def get_queryset(self):
        queryset = Country.objects.all().order_by("name")
        query_param = self.request.query_params.get("query")

        if query_param:
            queryset = queryset.filter(Q(name__icontains=query_param))

        return queryset


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = NoPagination

    def get_queryset(self):
        queryset = City.objects.all().order_by("name")
        query_param = self.request.query_params.get("query")

        if query_param:
            queryset = queryset.filter(Q(name__icontains=query_param))

        return queryset


class POIViewSet(viewsets.ModelViewSet):
    queryset = POI.objects.all()
    serializer_class = POISerializer
    pagination_class = NoPagination

    def get_queryset(self):
        queryset = POI.objects.all().order_by("name")
        query_param = self.request.query_params.get("query")

        if query_param:
            queryset = queryset.filter(Q(name__icontains=query_param))

        return queryset
