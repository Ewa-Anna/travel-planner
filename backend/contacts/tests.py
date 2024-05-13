from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Friendship

User = get_user_model()


class FriendshipAPITests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1", email="user1@example.com")
        self.user2 = User.objects.create(username="user2", email="user2@example.com")
        self.client = APIClient()

    def test_add_friend(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            "/contacts/friendships/", {"user": self.user1.pk, "friend": self.user2.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Friendship.objects.filter(user=self.user1, friend=self.user2).exists()
        )

    def test_add_self_as_friend(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            "/contacts/friendships/", {"user": self.user1.pk, "friend": self.user1.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            Friendship.objects.filter(user=self.user1, friend=self.user1).exists()
        )

    def test_duplicate_friendship(self):
        self.client.force_authenticate(user=self.user1)
        Friendship.objects.create(user=self.user1, friend=self.user2)
        response = self.client.post(
            "/contacts/friendships/", {"user": self.user1.pk, "friend": self.user2.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            Friendship.objects.filter(user=self.user1, friend=self.user2).count(), 1
        )
