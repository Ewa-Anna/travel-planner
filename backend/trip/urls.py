from django.urls import path

from .views import (
    TripView,
    TripDetailView,
    ParticipantView,
    ParticipantDetailView,
    ParticipantTripsView,
    MyTripsListView,
)


app_name = "trip"

urlpatterns = [
    path("trips/", TripView.as_view(), name="trip-list-create"),
    path("trips/<int:pk>/", TripDetailView.as_view(), name="trip-detail"),
    path("participants/", ParticipantView.as_view(), name="participant-list-create"),
    path(
        "participants/<int:pk>/",
        ParticipantDetailView.as_view(),
        name="participant-detail",
    ),
    path(
        "participants/<int:pk>/trips/",
        ParticipantTripsView.as_view(),
        name="participant-trips",
    ),
    path(
        "my_trips_organizer/",
        MyTripsListView.as_view(),
        name="my_trips_organizer",
    ),
]
