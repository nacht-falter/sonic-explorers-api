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

        print(str(f"\n{self.id()}"))

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
