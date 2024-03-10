import json

from django.test import TestCase
from django.urls import reverse
from django_rest_passwordreset.models import ResetPasswordToken

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import CustomUser, Profile
from .serializers import ChangePasswordSerializer
from .utils import CustomTokenGenerator


class CustomTokenObtainPairViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_token_obtain_pair(self):
        # pylint: disable=W0612
        user = CustomUser.objects.create_user(  # noqa: F841
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
        self.assertTrue(CustomUser.objects.filter(username="newuser").exists())
        self.assertTrue(Profile.objects.filter(user__username="newuser").exists())

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


class ProfileViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test_user", email="test@example.com", password="test_password"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio="Test bio",
            photo="https://example.com/test.jpg",
            birthdate="1990-01-01",
        )

    def test_get_profile(self):
        url = reverse("authx:profile")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "Test bio")
        self.assertEqual(response.data["photo"], "https://example.com/test.jpg")
        self.assertEqual(response.data["birthdate"], "1990-01-01")

    def test_update_profile(self):
        url = reverse("authx:profile")
        updated_data = {
            "bio": "Updated bio",
            "photo": "https://example.com/updated.jpg",
            "birthdate": "1995-01-01",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, "Updated bio")
        self.assertEqual(self.profile.photo, "https://example.com/updated.jpg")
        self.assertEqual(str(self.profile.birthdate), "1995-01-01")


class ChangePasswordViewTestCase(APITestCase):
    def test_change_password_success(self):
        user = CustomUser.objects.create_user(
            username="testuser", password="old_password"
        )
        self.client.login(username="testuser", password="old_password")

        url = reverse("authx:change_password", kwargs={"pk": user.pk})
        data = {
            "old_password": "old_password",
            "new_password": "new_password",
            "new_password_confirm": "new_password",
        }
        response = self.client.put(
            url, json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Your password has been changed.")
        user.refresh_from_db()
        self.assertTrue(user.check_password("new_password"))

    def test_change_password_wrong_old_password(self):
        user = CustomUser.objects.create_user(
            username="testuser", password="old_password"
        )
        self.client.login(username="testuser", password="old_password")

        url = reverse("authx:change_password", kwargs={"pk": user.pk})
        data = {
            "old_password": "wrong_old_password",
            "new_password": "new_password",
            "new_password_confirm": "new_password",
        }
        response = self.client.put(
            url, json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("old_password", response.data)


class ChangePasswordSerializerTestCase(APITestCase):
    def test_password_min_length_validation(self):
        serializer = ChangePasswordSerializer(
            data={"new_password": "pass", "confirm_new_password": "pass"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("new_password", serializer.errors)

    def test_password_contain_letter_validation(self):
        serializer = ChangePasswordSerializer(
            data={"new_password": "1234567890", "confirm_new_password": "1234567890"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("new_password", serializer.errors)


class DeactivateAccountViewTestCase(APITestCase):
    def test_deactivate_account_success(self):
        user = CustomUser.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        url = reverse("authx:deactivate-account")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Account deactivated successfully.")
        user.refresh_from_db()
        self.assertFalse(user.is_active)


class PasswordResetConfirmAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )
        self.token_generator = CustomTokenGenerator()
        self.token = self.token_generator.generate_token()
        ResetPasswordToken.objects.create(key=self.token, user=self.user)

    def test_password_reset_success(self):
        url = reverse("authx:password_reset_confirm")
        data = {
            "new_password": "new_password",
            "confirm_new_password": "new_password",
            "token": self.token,
        }
        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], "Password reset successfully")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new_password"))

    def test_invalid_token(self):
        url = reverse("authx:password_reset_confirm")
        data = {
            "new_password": "new_password",
            "confirm_new_password": "new_password",
            "token": "invalid_token",
        }
        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
