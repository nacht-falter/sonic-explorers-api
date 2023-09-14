from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to="images/avatars/",
        default="../default_profile_p5rke8",
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.owner}'s profile"
