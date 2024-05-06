from rest_framework import serializers

from .models import Accommodation, Transportation


class AccommodationSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Accommodation
        fields = [
            "id",
            "name",
            "location",
            "details",
            "price_per_night",
            "checkin_date",
            "checkout_date",
            "amenities",
            "total_price",
            "created_by",
        ]

    def get_total_price(self, obj):
        number_of_nights = (obj.checkout_date - obj.checkin_date).days
        total_price = obj.price_per_night * number_of_nights
        return total_price


class TransportationSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Transportation
        fields = [
            "id",
            "name",
            "departure_location",
            "arrival_location",
            "departure_time",
            "arrival_time",
            "description",
            "price",
            "type",
            "created_by",
        ]
