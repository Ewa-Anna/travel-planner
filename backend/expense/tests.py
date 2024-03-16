from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from trip.models import Trip
from authx.models import CustomUser
from .models import Expense


class ExpenseViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.trip = Trip.objects.create(
            name="Trip Test",
            start_date="2024-10-12",
            end_date="2024-10-30",
            organizer=self.user,
        )
        self.expense_data = {
            "trip": self.trip,
            "category": "accommodation",
            "amount": "100.00",
            "currency": "USD",
            "details": "Hotel stay",
        }
        self.expense = Expense.objects.create(**self.expense_data)

    def test_create_expense(self):
        self.client.force_login(self.user)
        data = {
            "trip": self.trip.pk,
            "category": "accommodation",
            "amount": "1000.00",
            "currency": "PLN",
        }
        url = reverse("expense:expense-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 2)

    def test_list_expense(self):
        self.client.force_login(self.user)
        url = reverse("expense:expense-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_expense(self):
        self.client.force_login(self.user)
        url = reverse("expense:expense-detail", kwargs={"pk": self.expense.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["category"], self.expense_data["category"])

    def test_update_expense(self):
        self.client.force_login(self.user)
        updated_data = {
            "trip": self.trip.pk,
            "category": "transportation",
            "amount": "50.00",
            "currency": "EUR",
            "details": "Taxi fare",
        }
        url = reverse("expense:expense-detail", kwargs={"pk": self.expense.pk})
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.category, updated_data["category"])

    def test_delete_expense(self):
        self.client.force_login(self.user)
        url = reverse("expense:expense-detail", kwargs={"pk": self.expense.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 0)
