from django.db import models
from django.contrib.auth.models import User
from sounds.models import Sound


class Like(models.Model):
    """Like model. Related to Sound and User models."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sound = models.ForeignKey(
        Sound, on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["owner", "sound"]

    def __str__(self):
        return f"{self.id} {self.owner} likes {self.sound}"
