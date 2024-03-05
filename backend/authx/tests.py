from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser


class CustomTokenObtainPairViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_token_obtain_pair(self):
        user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )

        response = self.client.post(
            reverse("authx:token_obtain_pair"),
            {"username": "testuser", "password": "password123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_credentials(self):
        response = self.client.post(
            reverse("authx:token_obtain_pair"),
            {"username": "invaliduser", "password": "invalidpassword"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration(self):
        response = self.client.post(
            reverse("authx:authx_register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "newpassword123",
                "password_confirm": "newpassword123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, "newuser")

    def test_password_mismatch(self):
        response = self.client.post(
            reverse("authx:authx_register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
                "password_confirm": "differentpassword",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_unique_email_validation(self):
        CustomUser.objects.create_user(
            username="existinguser", email="existing@example.com", password="password"
        )

        response = self.client.post(
            reverse("authx:authx_register"),
            {
                "username": "newuser",
                "email": "existing@example.com",
                "password": "newpassword123",
                "password_confirm": "newpassword123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["email"][0], "This field must be unique.")
