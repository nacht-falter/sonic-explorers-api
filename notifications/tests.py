from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Notification
from sounds.models import Sound
from likes.models import Like
from comments.models import Comment
from follows.models import Follow
from reports.models import Report


class NotificationSignalTest(APITestCase):
    """Tests for notification creation signals."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.sound = Sound.objects.create(
            owner=self.user2,
            title="testsound",
            latitude=0.0,
            longitude=0.0,
        )

        print(f"\n{self.id()}")

    def test_notification_created_for_new_like(self):
        Like.objects.create(owner=self.user1, sound=self.sound)
        notification = Notification.objects.first()
        count = Notification.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(notification.owner, self.user2)
        self.assertEqual(notification.category, "like")
        self.assertEqual(notification.title, "You have a new like!")

    def test_notification_created_for_new_comment(self):
        Comment.objects.create(
            owner=self.user1, sound=self.sound, content="test comment"
        )
        notification = Notification.objects.first()
        count = Notification.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(notification.owner, self.user2)
        self.assertEqual(notification.category, "comment")
        self.assertEqual(notification.title, "You have a new comment!")

    def test_notification_created_for_new_follow(self):
        Follow.objects.create(owner=self.user1, followed=self.user2)
        notification = Notification.objects.first()
        count = Notification.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(notification.owner, self.user2)
        self.assertEqual(notification.category, "follow")
        self.assertEqual(notification.title, "You have a new follower!")

    def test_notification_created_for_new_sound(self):
        Follow.objects.create(owner=self.user1, followed=self.user2)
        Sound.objects.create(
            owner=self.user2,
            title="testsound2",
            latitude=0.0,
            longitude=0.0,
        )
        notification = Notification.objects.filter(
            category="new_sound"
        ).first()
        count = Notification.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(notification.owner, self.user1)
        self.assertEqual(notification.category, "new_sound")
        self.assertEqual(notification.title, "You have a new sound!")

    def test_notification_created_for_new_report(self):
        self.user1.is_staff = True
        self.user1.save()
        Report.objects.create(
            owner=self.user2,
            sound=self.sound,
            flag="other",
            content="test report",
        )
        notification = Notification.objects.first()
        count = Notification.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(notification.owner, self.user1)
        self.assertEqual(notification.category, "report")
        self.assertEqual(
            notification.title, f"New report for sound '{self.sound.title}'"
        )


class NotificationListTest(APITestCase):
    """Tests for NotificationList view."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.client = APIClient()
        self.url = reverse("notifications")
        self.notification1 = Notification.objects.create(
            owner=self.user1,
            category="like",
            title="test notification",
            content="test",
        )
        self.notification2 = Notification.objects.create(
            owner=self.user2,
            category="like",
            title="test notification",
            content="test",
        )

        print(f"\n{self.id()}")

    def test_user_can_list_own_notifications(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_user_cannot_create_notification(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.post(
            self.url,
            {
                "category": "like",
                "title": "test notification",
                "content": "test",
            },
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )


class NotificationDetailTest(APITestCase):
    """Tests for NotificationDetail view."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.notification1 = Notification.objects.create(
            owner=self.user1,
            category="like",
            title="test notification",
            content="test",
        )
        self.notification2 = Notification.objects.create(
            owner=self.user2,
            category="like",
            title="test notification",
            content="test",
        )
        self.client = APIClient()

        print(f"\n{self.id()}")

    def test_user_can_retrieve_own_notification(self):
        self.client.login(username="testuser1", password="testpassword")
        url = reverse("notification_detail", args=[self.notification1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.notification1.id)

    def test_user_cannot_retrieve_another_users_notification(self):
        self.client.login(username="testuser1", password="testpassword")
        url = reverse("notification_detail", args=[self.notification2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_update_is_read_field(self):
        self.client.login(username="testuser1", password="testpassword")
        url = reverse("notification_detail", args=[self.notification1.id])
        response = self.client.patch(url, {"is_read": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_read"])

    def test_user_can_delete_own_notification(self):
        self.client.login(username="testuser1", password="testpassword")
        url = reverse("notification_detail", args=[self.notification1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_another_users_notification(self):
        self.client.login(username="testuser1", password="testpassword")
        url = reverse("notification_detail", args=[self.notification2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
