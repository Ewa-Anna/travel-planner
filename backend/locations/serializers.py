from rest_framework import serializers

from .models import Country, City, POI


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "iso_code", "currency", "primary_language", "flag"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "country",
            "population",
            "latitude",
            "longitude",
            "region",
        ]


class CityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name"]


class POISerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = POI
        fields = [
            "id",
            "name",
            "description",
            "city",
            "location_latitude",
            "location_longitude",
            "opening_hours",
        ]
