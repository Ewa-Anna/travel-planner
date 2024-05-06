from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Accommodation, Transportation


User = get_user_model()


class AccommodationViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.accommodation1 = Accommodation.objects.create(
            name="Hotel ABC",
            location="City XYZ",
            details="Details about the hotel",
            price_per_night=100,
            checkin_date="2024-03-20",
            checkout_date="2024-03-25",
            amenities="Amenities of the hotel",
            created_by=self.user,
        )
        self.client = APIClient()

    def test_list_accommodations(self):
        self.client.force_login(self.user)
        response = self.client.get("/services/accommodations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_accommodation(self):
        self.client.force_login(self.user)
        response = self.client.get(
            f"/services/accommodations/{self.accommodation1.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Hotel ABC")

    def test_create_accommodation(self):
        self.client.force_login(self.user)
        data = {
            "name": "New Hotel",
            "location": "New City",
            "details": "Details about the new hotel",
            "price_per_night": 120,
            "checkin_date": "2024-03-28",
            "checkout_date": "2024-03-30",
            "amenities": "Amenities of the new hotel",
        }
        response = self.client.post("/services/accommodations/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Accommodation.objects.count(), 2)

    def test_update_accommodation(self):
        self.client.force_login(self.user)
        data = {
            "name": "Updated Hotel",
            "location": "New City",
            "details": "",
            "price_per_night": 150,
            "checkin_date": "2024-03-28",
            "checkout_date": "2024-03-30",
            "amenities": "",
        }
        response = self.client.put(
            f"/services/accommodations/{self.accommodation1.pk}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Hotel")
        self.assertEqual(response.data["price_per_night"], "150.00")

    def test_delete_accommodation(self):
        self.client.force_login(self.user)
        response = self.client.delete(
            f"/services/accommodations/{self.accommodation1.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Accommodation.objects.count(), 0)


class TransportationViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.transportation1 = Transportation.objects.create(
            name="Flight XYZ",
            departure_location="City A",
            arrival_location="City B",
            departure_time="2024-03-20T10:00:00Z",
            arrival_time="2024-03-20T12:00:00Z",
            description="Description of the flight",
            price=200,
            type="plane",
            created_by=self.user,
        )
        self.client = APIClient()

    def test_list_transportations(self):
        self.client.force_login(self.user)
        response = self.client.get("/services/transportations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_transportation(self):
        self.client.force_login(self.user)
        response = self.client.get(
            f"/services/transportations/{self.transportation1.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Flight XYZ")

    def test_create_transportation(self):
        self.client.force_login(self.user)
        data = {
            "name": "New Flight",
            "departure_location": "City C",
            "arrival_location": "City D",
            "departure_time": "2024-03-21T10:00:00Z",
            "arrival_time": "2024-03-21T12:00:00Z",
            "description": "Description of the new flight",
            "price": 250,
            "type": "plane",
        }
        response = self.client.post("/services/transportations/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transportation.objects.count(), 2)

    def test_update_transportation(self):
        self.client.force_login(self.user)
        data = {
            "name": "Updated Flight",
            "departure_location": "City C",
            "arrival_location": "City D",
            "departure_time": "2024-03-21T10:00:00Z",
            "arrival_time": "2024-03-21T12:00:00Z",
            "description": "Description of the new flight",
            "price": 220,
            "type": "plane",
        }
        response = self.client.put(
            f"/services/transportations/{self.transportation1.pk}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Flight")
        self.assertEqual(response.data["price"], "220.00")

    def test_delete_transportation(self):
        self.client.force_login(self.user)
        response = self.client.delete(
            f"/services/transportations/{self.transportation1.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transportation.objects.count(), 0)
