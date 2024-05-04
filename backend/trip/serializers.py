from rest_framework import serializers

from services.serializers import AccommodationSerializer, TransportationSerializer
from services.models import Accommodation, Transportation
from locations.models import POI
from locations.serializers import POIViewSerializer
from authx.serializers import CustomUserSerializer
from authx.models import CustomUser
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


class ParticipantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id", "trip", "participant"]


class ParticipantViewSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="participant.first_name", read_only=True)
    last_name = serializers.CharField(source="participant.last_name", read_only=True)

    class Meta:
        model = Participant
        fields = ["participant", "first_name", "last_name"]


class OrganizerViewSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name"]


class TripSerializer(serializers.ModelSerializer):
    organizer = OrganizerViewSerializer(read_only=True)
    participants = ParticipantViewSerializer(many=True, read_only=True)
    trip_length = serializers.SerializerMethodField(read_only=True)
    pois = POIViewSerializer(many=True, read_only=True)
    accommodations = AccommodationSerializer(many=True, required=False, read_only=True)
    transportations = TransportationSerializer(
        many=True, required=False, read_only=True
    )

    class Meta:
        model = Trip
        fields = [
            "id",
            "name",
            "visibility",
            "start_date",
            "end_date",
            "trip_length",
            "organizer",
            "participants",
            "pois",
            "accommodations",
            "transportations",
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


class TripCreateSerializer(serializers.ModelSerializer):
    organizer = serializers.SerializerMethodField()
    participants = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    pois = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    accommodations = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    transportations = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

    class Meta:
        model = Trip
        # pylint: disable=R0801
        fields = [
            "id",
            "name",
            "visibility",
            "start_date",
            "end_date",
            "organizer",
            "participants",
            "pois",
            "accommodations",
            "transportations",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["organizer"] = request.user

        participants_ids = validated_data.pop("participants", [])
        pois_ids = validated_data.pop("pois", [])
        accommodations_ids = validated_data.pop("accommodations", [])
        transportations_ids = validated_data.pop("transportations", [])

        trip = Trip.objects.create(**validated_data)

        for participant_id in participants_ids:
            Participant.objects.create(trip=trip, participant_id=participant_id)

        for poi_id in pois_ids:
            poi = POI.objects.get(id=poi_id)
            trip.pois.add(poi)

        for accommodation_id in accommodations_ids:
            accommodation = Accommodation.objects.get(id=accommodation_id)
            trip.accommodations.add(accommodation)

        for transportation_id in transportations_ids:
            transportation = Transportation.objects.get(id=transportation_id)
            trip.transportations.add(transportation)

        return trip

    def update(self, instance, validated_data):
        participants_data = validated_data.pop("participants", None)
        pois_data = validated_data.pop("pois", None)
        accommodations_data = validated_data.pop("accommodations", None)
        transportations_data = validated_data.pop("transportations", None)

        instance.name = validated_data.get("name", instance.name)
        instance.visibility = validated_data.get("visibility", instance.visibility)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)

        if participants_data is not None:
            instance.participants.all().delete()
            for participant_id in participants_data:
                participant = CustomUser.objects.get(id=participant_id)
                Participant.objects.create(trip=instance, participant=participant)

        if pois_data is not None:
            instance.pois.clear()
            for poi_id in pois_data:
                poi = POI.objects.get(id=poi_id)
                instance.pois.add(poi)

        if accommodations_data is not None:
            instance.accommodations.clear()
            for accommodation_id in accommodations_data:
                accommodation = Accommodation.objects.get(id=accommodation_id)
                instance.accommodations.add(accommodation)

        if transportations_data is not None:
            instance.transportations.clear()
            for transportation_id in transportations_data:
                transportation = Transportation.objects.get(id=transportation_id)
                instance.transportations.add(transportation)

        instance.save()
        return instance

    def get_organizer(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return CustomUserSerializer(request.user).data
        return None

    def validate(self, attrs):
        participants_data = attrs.get("participants", [])
        if not participants_data:
            raise serializers.ValidationError("At least one participant is required.")

        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if end_date <= start_date:
            raise serializers.ValidationError(
                "End date must be greater than the start date."
            )

        return attrs
