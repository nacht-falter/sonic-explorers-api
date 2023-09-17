from django.contrib.auth.models import User
from django.urls import reverse
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Like
from sounds.models import Sound


class LikeListTest(APITestCase):
    """Tests for the LikeList view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.url = reverse("likes")
        self.sound = Sound.objects.create(
            owner=self.user,
            title="testtitle",
            description="testdescription",
            latitude=0.0,
            longitude=0.0,
        )

        print(f"\n{self.id()}")

    def test_user_can_list_likes(self):
        Like.objects.create(owner=self.user, sound=self.sound)
        response = self.client.get(self.url)
        count = Like.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, 200)

    def test_user_can_like_sound(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, {"sound": self.sound.id})
        count = Like.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_like_sound_twice(self):
        self.client.login(username="testuser", password="testpassword")
        Like.objects.create(owner=self.user, sound=self.sound)

        # Instructions for avoiding TransactionManagementError from:
        # https://stackoverflow.com/a/23326971
        try:
            with transaction.atomic():
                response = self.client.post(self.url, {"sound": self.sound.id})
        except IntegrityError:
            pass

        count = Like.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "You have already liked this sound.", response.data["detail"]
        )


class LikeDetailTest(APITestCase):
    """Tests for the LikeDetail view."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.client = APIClient()
        self.sound = Sound.objects.create(
            owner=self.user1,
            title="testtitle",
            description="testdescription",
            latitude=0.0,
            longitude=0.0,
        )
        self.like = Like.objects.create(owner=self.user1, sound=self.sound)
        self.url = reverse("like_detail", args=[self.like.id])

        print(f"\n{self.id()}")

    def test_user_can_unlike_sound(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.delete(self.url, {"sound": self.sound.id})
        count = Like.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_another_users_like(self):
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.delete(self.url, {"sound": self.sound.id})
        count = Like.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            "You do not have permission to perform this action.",
            response.data["detail"],
        )
