from rest_framework import serializers

from .models import Country, City, POI


class CountryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


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


class CityViewSerializer(serializers.ModelSerializer):
    country = CountryNameSerializer(read_only=True)

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


class POIViewSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    city = CityNameSerializer(read_only=True)

    class Meta:
        model = POI
        fields = [
            "id",
            "name",
            "city",
            "description",
            "location_latitude",
            "location_longitude",
            "opening_hours",
        ]


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
