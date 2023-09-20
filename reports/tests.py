from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from sounds.models import Sound
from .models import Report


class ReportListTest(APITestCase):
    """Tests for ReportList view."""

    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staffuser", password="staffpassword", is_staff=True
        )
        self.sound = Sound.objects.create(
            owner=self.staff_user,
            title="testsound",
            latitude=0.0,
            longitude=0.0,
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Report.objects.create(
            owner=self.user,
            sound=self.sound,
            flag="other",
        )
        self.client = APIClient()

        print(f"\n{self.id()}")

    def test_staff_user_can_view_reports(self):
        self.client.login(username="staffuser", password="staffpassword")
        response = self.client.get(reverse("reports"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_regular_user_cannot_view_reports(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("reports"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_can_create_report(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("reports"),
            {
                "sound": self.sound.id,
                "flag": "other",
                "content": "test report",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 2)


class ReportDetailTest(APITestCase):
    """Tests for ReportDetail view."""

    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staffuser", password="staffpassword", is_staff=True
        )
        self.sound = Sound.objects.create(
            owner=self.staff_user,
            title="testsound",
            latitude=0.0,
            longitude=0.0,
        )
        self.report = Report.objects.create(
            owner=self.staff_user,
            sound=self.sound,
            flag="other",
            content="test report",
        )
        self.client = APIClient()

        print(f"\n{self.id()}")

    def test_staff_user_can_delete_report(self):
        self.client.login(username="staffuser", password="staffpassword")
        response = self.client.delete(
            reverse("report_detail", args={self.sound.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Report.objects.count(), 0)
