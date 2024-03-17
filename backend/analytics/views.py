from collections import Counter
from datetime import datetime

from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, DurationField

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authx.models import CustomUser
from trip.models import Trip
from locations.models import POI
from expense.models import Expense
from journal.models import Review
from services.models import Accommodation

from .utils import calculate_total_time_spent


class AnalyticsReview(APIView):
    """
    Returns top5 reviews with the highest number of likes.
    """

    def get_most_liked_review(self):
        most_liked_reviews = Review.objects.filter(visibility="public").order_by(
            "-likes"
        )[:5]
        return most_liked_reviews

    def get(self, request, *args, **kwargs):
        most_liked_reviews = self.get_most_liked_review()
        if most_liked_reviews:
            reviews_data = []
            for review in most_liked_reviews:
                review_data = {
                    "id": review.id,
                    "user": review.user.username,
                    "trip": review.trip.name,
                    "rating": review.rating,
                    "comment": review.comment,
                    "date": review.date.strftime("%Y-%m-%d %H:%M:%S"),
                    "likes": review.likes,
                    "dislikes": review.dislikes,
                    "recommended": review.recommended,
                    "pros": review.pros,
                    "cons": review.cons,
                    "visibility": review.visibility,
                }
                reviews_data.append(review_data)
            return Response(reviews_data, status=status.HTTP_200_OK)

        return Response(
            {"detail": "No reviews found"}, status=status.HTTP_404_NOT_FOUND
        )


class AnalyticsExpense(APIView):
    def get(self, request, trip_id):
        total_expenses = (
            Expense.objects.filter(trip_id=trip_id).aggregate(total=Sum("amount"))[
                "total"
            ]
            or 0
        )
        expense_by_category = (
            Expense.objects.filter(trip_id=trip_id)
            .values("category")
            .annotate(total=Sum("amount"))
        )
        return Response(
            {
                "total_expenses": total_expenses,
                "expenses_by_category": {
                    item["category"]: item["total"] for item in expense_by_category
                },
            }
        )


class PopularPOIs(APIView):
    def get(self, request):
        popular_pois = POI.objects.annotate(num_trips=Count("trips")).order_by(
            "-num_trips"
        )[:5]
        return Response(
            [{"name": poi.name, "num_trips": poi.num_trips} for poi in popular_pois]
        )


class PopularAccommodations(APIView):
    def get(self, request):
        popular_accommodations = Accommodation.objects.annotate(
            num_trips=Count("trips")
        ).order_by("-num_trips")[:5]
        return Response(
            [
                {"name": accommodation.name, "num_trips": accommodation.num_trips}
                for accommodation in popular_accommodations
            ]
        )


class AverageTripDurationView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        trips = Trip.objects.filter(organizer=request.user)
        durations = trips.annotate(
            duration=ExpressionWrapper(
                F("end_date") - F("start_date"), output_field=DurationField()
            )
        )
        avg_duration = durations.aggregate(avg_duration=Avg("duration"))

        avg_duration_days = (
            avg_duration.get("avg_duration").days
            if avg_duration.get("avg_duration")
            else None
        )

        return Response(
            {"average_trip_duration_days": avg_duration_days}, status=status.HTTP_200_OK
        )


class TimelineView(APIView):
    def get(self, request):
        current_year = datetime.now().year
        trips = Trip.objects.filter(start_date__year=current_year)
        data = []
        for trip in trips:
            trip_data = {
                "name": trip.name,
                "start_date": trip.start_date,
                "end_date": trip.end_date,
            }
            data.append(trip_data)

        return Response(data, status=status.HTTP_200_OK)


class MostVisitedCountries(APIView):
    """
    Most visited countries as an organizer.
    """

    def get(self, request):
        user_trips = Trip.objects.filter(organizer=request.user)
        country_trip_map = Counter()
        for trip in user_trips:
            trip_pois = trip.pois.all()
            trip_countries = set(poi.city.country for poi in trip_pois)
            for country in trip_countries:
                country_trip_map[country] += 1

        top_visited_countries = country_trip_map.most_common()
        data = [
            {"country": country.name, "trip_count": count}
            for country, count in top_visited_countries
        ]

        return Response(data)


class UserAnalyticsView(APIView):
    def get(self, request):
        total_time_spent = calculate_total_time_spent(request.user)
        return Response({"total_time_spent_in_h": total_time_spent})


class TotalUsers(APIView):
    def get(self, request):
        total_users_count = CustomUser.objects.count()
        return Response({"total_users": total_users_count})
