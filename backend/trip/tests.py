from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework import serializers

from .models import Trip, Participant
from .serializers import TripSerializer, ParticipantSerializer


User = get_user_model()


class TripParticipantTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            email="user1@example.com", username="user1", password="test_password"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", username="user2", password="test_password"
        )

        self.trip1 = Trip.objects.create(
            name="Trip 1",
            start_date="2024-01-01",
            end_date="2024-01-05",
            organizer=self.user1,
        )
        self.trip2 = Trip.objects.create(
            name="Trip 2",
            start_date="2024-02-01",
            end_date="2024-02-05",
            organizer=self.user2,
        )

        self.participant1 = Participant.objects.create(
            trip=self.trip1, participant=self.user1
        )
        self.participant2 = Participant.objects.create(
            trip=self.trip1, participant=self.user2
        )
        self.participant3 = Participant.objects.create(
            trip=self.trip2, participant=self.user1
        )

    def test_trip_model(self):
        trip = Trip.objects.get(id=self.trip1.id)
        self.assertEqual(trip.name, "Trip 1")

    def test_participant_model(self):
        participant = Participant.objects.get(id=self.participant1.id)
        self.assertEqual(participant.trip, self.trip1)
        self.assertEqual(participant.participant, self.user1)

    def test_participant_serializer(self):
        serializer = ParticipantSerializer(instance=self.participant1)
        self.assertEqual(serializer.data["trip"], self.trip1.id)
        self.assertEqual(serializer.data["participant"], self.user1.id)

    def test_trip_view(self):
        self.client.force_login(self.user1)
        response = self.client.get("/trip/trips/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_participant_view(self):
        self.client.force_login(self.user1)
        response = self.client.get("/trip/participants/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)

    def test_participant_trips_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(f"/trip/participants/{self.user1.id}/trips/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_organizer_filter(self):
        self.client.force_login(self.user1)
        response = self.client.get(f"/trip/trips/?organizer={self.user1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_participant_filter(self):
        self.client.force_login(self.user1)
        response = self.client.get(f"/trip/trips/?participant={self.user1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_update_trip(self):
        self.client.force_login(self.user1)
        data = {
            "name": "Updated Trip",
            "start_date": "2024-01-01",
            "end_date": "2024-01-05",
            "organizer": self.user1.id,
        }
        response = self.client.put(f"/trip/trips/{self.trip1.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Trip")

    def test_delete_trip(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f"/trip/trips/{self.trip1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_duplicate_participant(self):
        self.client.force_login(self.user1)
        data = {"trip": self.trip1.id, "participant": self.user1.id}
        response = self.client.post("/trip/participants/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_participant_creation(self):
        self.client.force_login(self.user1)
        data = {"participant": self.user1.id}
        response = self.client.post("/trip/participants/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_participant_details(self):
        self.client.force_login(self.user1)
        response = self.client.get(f"/trip/participants/{self.participant1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["participant"], self.user1.id)

    def test_participant_deletion(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f"/trip/participants/{self.participant1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/trip/trips/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        User.objects.all().delete()
        Trip.objects.all().delete()
        Participant.objects.all().delete()


class TripCreationTestCase(TestCase):
    def setUp(self):
        self.serializer = TripSerializer()
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.client = APIClient()

    def test_invalid_trip_creation(self):
        self.client.force_login(self.user)
        start_date = datetime(2024, 1, 10)
        end_date = datetime(2024, 1, 5)
        data = {
            "name": "Invalid Trip",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "organizer": self.user.id,
        }

        response = self.client.post("/trip/trips/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_end_date_greater_than_start_date(self):
        self.client.force_login(self.user)
        data = {
            "name": "Test Trip",
            "start_date": "2024-01-05",  
            "end_date": "2024-01-01"    
        }

        with self.assertRaises(serializers.ValidationError) as context:
            self.serializer.validate(data)

        expected_error_message = ["End date must be greater than the start date."]
        self.assertEqual(
            [str(error) for error in context.exception.detail],
            expected_error_message
        )

    def test_end_date_equal_to_start_date(self):
        self.client.force_login(self.user)
        data = {
            "name": "Test Trip",
            "start_date": "2024-01-01", 
            "end_date": "2024-01-01"     
        }

        with self.assertRaises(serializers.ValidationError) as context:
            self.serializer.validate(data)

        expected_error_message = ["End date must be greater than the start date."]
        self.assertEqual(
            [str(error) for error in context.exception.detail],
            expected_error_message
        )

    def test_end_date_greater_than_start_date_valid(self):
        self.client.force_login(self.user)        
        data = {
            "name": "Test Trip",
            "start_date": "2024-01-01", 
            "end_date": "2024-01-05"    
        }

        validated_data = self.serializer.validate(data)

        self.assertEqual(validated_data, data)