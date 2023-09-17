from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Sound
from django.core.files.uploadedfile import SimpleUploadedFile


class SoundListViewTests(APITestCase):
    """Tests for SoundList view.

    Instructions for DRF testing from:
    https://www.django-rest-framework.org/api-guide/testing/
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client = APIClient()
        self.url = reverse("sounds")
        self.data = {
            "title": "testtitle",
            "description": "testdescription",
            "image": "testimage",
            "latitude": 0.0,
            "longitude": 0.0,
        }

        print(f"\n{self.id()}")

    def test_user_can_list_sounds(self):
        Sound.objects.create(
            owner=self.user,
            title=self.data["title"],
            description=self.data["description"],
            latitude=self.data["latitude"],
            longitude=self.data["longitude"],
        )
        response = self.client.get(self.url)
        count = Sound.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, 200)

    def test_missing_audio_file_throws_error(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, self.data)
        count = Sound.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No file was submitted", response.data["audio_file"][0])

    def test_wrong_file_type_throws_error(self):
        self.client.login(username="testuser", password="testpassword")

        # Mock a file upload (https://stackoverflow.com/a/20508621)
        file = SimpleUploadedFile("test.txt", b"these are the file contents!")
        self.data["audio_file"] = file.file
        response = self.client.post(self.url, self.data)
        count = Sound.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Unsupported video format or file",
            response.data["audio_file"]["detail"],
        )


class SoundDetailViewTests(APITestCase):
    """Tests for SoundDetail view"""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
        )
        self.sound = Sound.objects.create(
            owner=self.user1,
            title="testtitle",
            description="testdescription",
            latitude=0.0,
            longitude=0.0,
        )
        self.data = {
            "title": "changedtitle",
            "description": "changeddescription",
            "latitude": 1.0,
            "longitude": 1.0,
        }

        # set URL for sound detail view (instructions from:
        # https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse)
        self.url = reverse("sound_detail", args=[self.sound.id])

        self.client = APIClient()

        print(str(f"\n{self.id()}"))

    def test_get_valid_sound(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.sound.title)

    def test_get_invalid_sound(self):
        url = reverse("sound_detail", args=[2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_can_update_owned_sound(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.data["title"])

    def test_user_cannot_upddate_another_users_sound(self):
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.put(self.url, self.data)
        sound = Sound.objects.get(id=self.sound.id)
        self.assertNotEqual(sound.title, self.data["title"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_owned_sound(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_unowned_sound(self):
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
