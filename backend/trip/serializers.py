from rest_framework import serializers

from locations.serializers import CityNameSerializer
from locations.models import POI
from .models import Trip, Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id", "trip", "participant"]

    def validate(self, attrs):
        """
        Validate that the participant is not already participating in the trip.
        """
        trip = attrs.get("trip")
        participant = attrs.get("participant")

        if Participant.objects.filter(trip=trip, participant=participant).exists():
            raise serializers.ValidationError(
                "Participant is already participating in the trip."
            )

        return attrs


class ParticipantViewSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="participant.first_name", read_only=True)
    last_name = serializers.CharField(source="participant.last_name", read_only=True)

    class Meta:
        model = Participant
        fields = ["participant", "first_name", "last_name"]


class POIViewSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    city = CityNameSerializer(read_only=True)

    class Meta:
        model = POI
        fields = ["name", "city"]


class TripSerializer(serializers.ModelSerializer):
    participants = ParticipantViewSerializer(many=True, read_only=True)
    trip_length = serializers.SerializerMethodField()
    pois = POIViewSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "trip_length",
            "organizer",
            "participants",
            "pois",
        ]

    def validate(self, attrs):
        """
        Validate that the end date is greater than the start date.
        """
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if end_date <= start_date:
            raise serializers.ValidationError(
                "End date must be greater than the start date."
            )

        return attrs

    def get_trip_length(self, obj):
        """
        Calculate the length of the trip in days.
        """
        length = (obj.end_date - obj.start_date).days
        if length == 1:
            days = "day"
        else:
            days = "days"

        return f"{length} {days}"
