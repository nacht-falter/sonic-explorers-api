from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from sonic_explorers_api.serializers import CurrentUserSerializer


class CurrentUserSerializerTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        # Print test id
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.id
        print(str(self.id()))

    def test_current_user_serializer(self):
        serializer = CurrentUserSerializer(self.user)
        data = serializer.data

        self.assertEqual(data["profile_id"], self.user.profile.id)
        self.assertEqual(data["profile_avatar"], self.user.profile.avatar.url)
        self.assertIn("default_profile", data["profile_avatar"])
