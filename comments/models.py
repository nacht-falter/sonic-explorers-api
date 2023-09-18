from django.db import models
from django.contrib.auth.models import User
from sounds.models import Sound


class Comment(models.Model):
    """Model representing a comment. Related to Users and Sounds.
    The string method contains a truncated version of the content.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sound = models.ForeignKey(
        Sound, on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        content = self.content
        return (
            # Instructions for conditionally truncating a string in Python
            # from: https://stackoverflow.com/a/52279347
            f"{self.owner.username} commented "
            f"'{content[:30] + ('...' if len(content) > 30 else '')}'"
            f" on sound {self.sound.id}"
        )
