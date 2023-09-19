from django.contrib.auth.models import User
from django.db import transaction
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Follow


class FollowListTest(APITestCase):
    """Tests for the FollowList view."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.client = APIClient()
        self.url = reverse("follows")

        print(f"\n{self.id()}")

    def test_user_can_list_follows(self):
        Follow.objects.create(owner=self.user1, followed=self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_follow(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.post(self.url, {"followed": self.user2.id})
        count = Follow.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count, 1)

    def test_logged_out_user_cannot_create_follow(self):
        response = self.client.post(self.url, {"followed": self.user2.id})
        count = Follow.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_self_follow(self):
        self.client.login(username="testuser1", password="testpassword")

        # Instructions for avoiding TransactionManagementError from:
        # https://stackoverflow.com/a/23326971
        with transaction.atomic():
            response = self.client.post(self.url, {"followed": self.user1.id})
        count = Follow.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_follow_same_user_twice(self):
        self.client.login(username="testuser1", password="testpassword")
        Follow.objects.create(owner=self.user1, followed=self.user2)
        with transaction.atomic():
            response = self.client.post(self.url, {"followed": self.user2.id})
        count = Follow.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FollowDetailTest(APITestCase):
    """Tests for the FollowDetail view."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.follow = Follow.objects.create(
            owner=self.user1, followed=self.user2
        )
        self.client = APIClient()
        self.url = reverse("follow_detail", args=[self.follow.id])

        print(f"\n{self.id()}")

    def test_user_can_retrieve_follow(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_own_follow(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.delete(self.url)
        count = Follow.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_another_users_follow(self):
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.delete(self.url)
        count = Follow.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
