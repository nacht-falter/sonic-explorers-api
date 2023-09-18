from django.db import models
from django.contrib.auth.models import User

CATEGORIES = [
    ("follow", "Follow"),
    ("comment", "Comment"),
    ("like", "Like"),
    ("new_sound", "New Sound"),
]


class Notification(models.Model):
    """Notification model representing a notification automatically sent to a
    user. Notifications are dynamically created, when sounds, likes, comments,
    and follows are created.
    """

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORIES, max_length=50)
    item_id = models.IntegerField(null=True)
    is_read = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)

    class Meta:
        ordering = ["-sent_at"]

    def __str__(self):
        return (
            f"{self.id} {self.get_category_display()} "
            f"notification for {self.owner}"
        )
