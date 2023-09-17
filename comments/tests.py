from django.contrib.auth.models import User
from django.urls import reverse
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Comment
from sounds.models import Sound


class CommentListTest(APITestCase):
    """Tests for the CommentList view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.url = reverse("comments")
        self.sound = Sound.objects.create(
            owner=self.user,
            title="testtitle",
            latitude=0.0,
            longitude=0.0,
        )
        self.data = {
            "owner": self.user.id,
            "sound": self.sound.id,
            "content": "testcontent",
        }

        print(f"\n{self.id()}")

    def test_user_can_list_comments(self):
        Comment.objects.create(owner=self.user, sound=self.sound)
        response = self.client.get(self.url)
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_can_create_comment(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, self.data)
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_comment(self):
        response = self.client.post(self.url, self.data)
        count = Comment.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentDetailTest(APITestCase):
    """Tests for the CommentDetail view."""

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
            latitude=0.0,
            longitude=0.0,
        )
        self.comment = Comment.objects.create(
            owner=self.user1, sound=self.sound
        )
        self.url = reverse("comment_detail", args=[self.comment.id])
        self.data = {
            "owner": self.user1.id,
            "sound": self.sound.id,
            "content": "testcontent",
        }
        self.updated_data = {
            "sound": self.sound.id,
            "content": "updatedcontent",
        }

        print(f"\n{self.id()}")

    def test_user_can_retrieve_comment(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_own_comment(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.put(self.url, self.updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_own_comment(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.delete(self.url)
        count = Comment.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_another_users_comment(self):
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.delete(self.url)
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
