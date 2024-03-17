from django.urls import path

from .views import (
    AnalyticsReview,
    AnalyticsExpense,
    PopularPOIs,
    PopularAccommodations,
    AverageTripDurationView,
    TimelineView,
    MostVisitedCountries,
    UserAnalyticsView,
    TotalUsers,
)

app_name = "analytics"

urlpatterns = [
    path("most-liked-review/", AnalyticsReview.as_view(), name="most-liked-review"),
    path(
        "expense-analytics/<int:trip_id>/",
        AnalyticsExpense.as_view(),
        name="expense-analytics",
    ),
    path("popular-pois/", PopularPOIs.as_view(), name="popular-pois"),
    path(
        "popular-accommodations/",
        PopularAccommodations.as_view(),
        name="popular-accommodations",
    ),
    path(
        "average-trip-duration/",
        AverageTripDurationView.as_view(),
        name="average-trip-duration",
    ),
    path("timeline/", TimelineView.as_view(), name="timeline"),
    path(
        "most-visited-countries/",
        MostVisitedCountries.as_view(),
        name="most-visited-countries",
    ),
    path("total-time-spent/", UserAnalyticsView.as_view(), name="total-time-spent"),
    path("total-users/", TotalUsers.as_view(), name="total-users"),
]
