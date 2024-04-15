from django.db import IntegrityError
from django.db.models import Q

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authx.models import CustomUser
from .serializers import (
    TripSerializer,
    ParticipantSerializer,
    TripCreateSerializer,
    ParticipantCreateSerializer,
)
from .models import Trip, Participant
from .permissions import IsOrganizerOrReadOnly


class TripView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TripCreateSerializer
        return TripSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        organizer_id = self.request.query_params.get("organizer")
        if organizer_id is not None:
            try:
                organizer_id = int(organizer_id)
                queryset = queryset.filter(organizer=organizer_id)
            except ValueError:
                pass

        participant_id = self.request.query_params.get("participant")
        if participant_id is not None:
            try:
                participant_id = int(participant_id)
                queryset = queryset.filter(participants__participant=participant_id)
            except ValueError:
                pass

        order_by = self.request.query_params.get("order_by")
        if order_by is not None:
            queryset = queryset.order_by(order_by)

        query = self.request.query_params.get("query")
        if query:
            queryset = queryset.filter(Q(name__icontains=query)).order_by("name")

        return queryset

    def list(self, request, *args, **kwargs):
        organizer_id = self.request.query_params.get("organizer")

        if organizer_id is not None:
            try:
                organizer_id = int(organizer_id)
                if not CustomUser.objects.filter(id=organizer_id).exists():
                    return Response(
                        {"success": False, "message": "Invalid organizer ID"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except ValueError:
                return Response(
                    {"success": False, "message": "Invalid organizer ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            trip_data = response.data
            trip = Trip.objects.get(id=trip_data["id"])
            trip_serializer = TripSerializer(
                trip, context=self.get_serializer_context()
            )
            trip_data.update(trip_serializer.data)
            return Response(
                {
                    "success": True,
                    "message": "Trip has been created successfully",
                    "result": trip_data,
                },
                status=status.HTTP_201_CREATED,
            )

        except IntegrityError as e:
            if "name" in str(e) and "organizer_id" in str(e):
                return Response(
                    {
                        "success": False,
                        "message": "A trip with this name already exists for this organizer.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {
                    "success": False,
                    "message": "An error occurred while creating the trip.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return TripCreateSerializer
        return TripSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        trip_data = response.data
        return Response(
            {
                "success": True,
                "message": "Trip has been updated successfully",
                "result": trip_data,
            }
        )

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        trip_data = response.data
        return Response(
            {
                "success": True,
                "message": "Trip has been updated successfully",
                "result": trip_data,
            }
        )


class ParticipantView(generics.ListCreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ParticipantCreateSerializer
        return ParticipantSerializer


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


class MyTripsListView(generics.ListAPIView):
    """
    Returns list of trips that currently logged in user is an organizer or participant.
    """

    serializer_class = TripSerializer

    def get_queryset(self):
        user = self.request.user
        user_type = self.request.query_params.get("user_type", "organizer")
        query = self.request.query_params.get("query", None)

        if user_type == "organizer":
            queryset = Trip.objects.filter(organizer=user).order_by("name")
        elif user_type == "participant":
            queryset = Trip.objects.filter(participants__participant=user).order_by(
                "name"
            )
        else:
            return Trip.objects.none()

        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset
