from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from follows.models import Follow


class ProfileSerializerTest(APITestCase):
    """Tests for ProfileSerializer."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.profile = self.user2.profile
        self.url = reverse("profile_detail", args=[self.profile.id])
        self.client = APIClient()

        print(f"\n{self.id()}")

    def test_get_follow_id_method_returns_follow_id(self):
        self.client.login(username="testuser1", password="testpassword")
        follow = Follow.objects.create(owner=self.user1, followed=self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.data["follow_id"], follow.id)

    def test_get_follow_id_method_returns_none_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertIsNone(response.data["follow_id"])
