from django.contrib.auth.models import User
from rest_framework.test import APITestCase
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
