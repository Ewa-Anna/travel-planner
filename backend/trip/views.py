from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import TripSerializer, ParticipantSerializer
from .models import Trip, Participant


class TripView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organizer_id = self.request.query_params.get("organizer")
        participant_id = self.request.query_params.get("participant")

        queryset = Trip.objects.all()

        if organizer_id is not None:
            try:
                organizer_id = int(organizer_id)
                queryset = queryset.filter(organizer=organizer_id)
            except ValueError:
                return Response(
                    {"error": "Invalid organizer ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if participant_id is not None:
            try:
                participant_id = int(participant_id)
                queryset = queryset.filter(participants__participant=participant_id)
            except ValueError:
                return Response(
                    {"error": "Invalid participant ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return queryset


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]


class ParticipantView(generics.ListCreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]


class ParticipantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]


class ParticipantTripsView(generics.ListAPIView):
    """
    Returns list of trips for given participant.
    """

    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        participant_id = self.kwargs.get("pk")
        return Trip.objects.filter(participants__participant=participant_id)


class MyTripsOrganizerListView(generics.ListAPIView):
    serializer_class = TripSerializer

    def get_queryset(self):
        return Trip.objects.filter(organizer=self.request.user)


class MyTripsParticipantListView(generics.ListAPIView):
    serializer_class = TripSerializer

    def get_queryset(self):
        return Trip.objects.filter(participants__participant=self.request.user)
