from django.db import models
from django.contrib.auth.models import User


class Sound(models.Model):
    """Sound model. Includes method for audio processing and geolocation."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    audio_file = models.FileField()
    image = models.ImageField(
        upload_to="images/",
        default="../default_sound_image_jlklol",
        blank=True,
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} {self.title}"
