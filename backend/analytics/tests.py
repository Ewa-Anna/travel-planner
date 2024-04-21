from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from expense.models import Expense
from journal.models import Review
from trip.models import Trip
from locations.models import POI, City, Country
from services.models import Accommodation
from authx.models import CustomUser


class TestAnalyticsReview(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.trip = Trip.objects.create(
            name="Test Trip",
            start_date="2024-05-11",
            end_date="2024-05-15",
            organizer=self.user,
        )
        self.review_data = {
            "user": self.user,
            "trip": self.trip,
            "rating": 7,
            "comment": "Test review",
            "date": datetime.now(),
            "likes": 5,
            "dislikes": 1,
            "recommended": True,
            "pros": "Pros",
            "cons": "Cons",
            "visibility": "public",
        }
        self.review = Review.objects.create(**self.review_data)

    def test_get_most_liked_review(self):
        url = reverse("analytics:most-liked-review")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.review.id)


class TestAnalyticsExpense(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.trip = Trip.objects.create(
            name="Test Trip",
            start_date="2024-01-11",
            end_date="2024-01-15",
            organizer=self.user,
        )
        self.expense_data = {
            "trip": self.trip,
            "amount": 100,
            "category": "Food",
        }
        self.expense = Expense.objects.create(**self.expense_data)

    def test_get_expense_by_category(self):
        url = reverse("analytics:expense-analytics", kwargs={"trip_id": self.trip.id})
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_expenses"], 100)
        self.assertIn("Food", response.data["expenses_by_category"])
        self.assertEqual(response.data["expenses_by_category"]["Food"], 100)


class TestPopularPOIs(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="test_user", password="testpassword123"
        )
        self.country = Country.objects.create(name="Country")
        self.city = City.objects.create(name="City", country=self.country)
        self.poi = POI.objects.create(name="Test POI", city=self.city)

    def test_get_popular_pois(self):
        url = reverse("analytics:popular-pois")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.poi.name)


class TestPopularAccommodations(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.accommodation = Accommodation.objects.create(
            name="Test Accommodation",
            location="Test Location",
            details="Details about the hotel",
            price_per_night=75,
            checkin_date="2024-03-20",
            checkout_date="2024-03-25",
        )

    def test_get_popular_accommodations(self):
        url = reverse("analytics:popular-accommodations")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.accommodation.name)


class TestAverageTripDurationView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.trip = Trip.objects.create(
            name="Test Trip",
            start_date="2024-05-11",
            end_date="2024-05-15",
            organizer=self.user,
        )

    def test_get_average_trip_duration(self):
        url = reverse("analytics:average-trip-duration")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("average_trip_duration_days", response.data)


class TestTimelineView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.trip = Trip.objects.create(
            name="Test Trip",
            start_date="2024-01-01",
            end_date="2024-01-05",
            organizer=self.user,
        )

    def test_get_timeline(self):
        url = reverse("analytics:timeline")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("name", response.data[0])
        self.assertIn("start_date", response.data[0])
        self.assertIn("end_date", response.data[0])


class TestMostVisitedCountries(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.trip = Trip.objects.create(
            name="Test Trip",
            start_date="2024-04-11",
            end_date="2024-04-15",
            organizer=self.user,
        )
        self.country = Country.objects.create(name="Country")
        self.city = City.objects.create(name="City", country=self.country)
        self.poi = POI.objects.create(name="Test POI", city=self.city)
        self.trip.pois.add(self.poi)

    def test_get_most_visited_countries(self):
        url = reverse("analytics:most-visited-countries-organizer")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("country", response.data[0])
        self.assertIn("trip_count", response.data[0])


class TestUserAnalyticsView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_get_user_analytics(self):
        url = reverse("analytics:total-time-spent")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_time_spent_in_h", response.data)


class TestTotalUsers(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_get_total_users(self):
        self.client.force_login(self.user)
        url = reverse("analytics:total-users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_users", response.data)
