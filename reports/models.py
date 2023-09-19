from django.db import models
from django.contrib.auth.models import User
from sounds.models import Sound


class Report(models.Model):
    """Report model representing reports for community guideline violations
    or other concerns."""

    # Flag choices inspired by SoundCloud's report page:
    # https://m.soundcloud.com/pages/report-content
    FLAG_CHOICES = [
        ("hate", "Hate speech"),
        ("illegal", "Illegal/extremist content"),
        ("violence", "Violent content"),
        ("pornographic", "Pornographic Content"),
        ("harassment", "Harassment or bullying"),
        ("privacy", "Privacy violation"),
        ("property", "Intellectual property violation"),
        ("other", "Other"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sound = models.ForeignKey(
        Sound, on_delete=models.CASCADE, related_name="reports"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    flag = models.CharField(choices=FLAG_CHOICES, max_length=50)
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.id} {self.owner} flagged {self.sound.title} as {self.flag}"
        )
