from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    """Model representing a follow relationship between users.
    The specified constraints prevent users from following the same
    user more than once and from following themselves.
    """

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followed_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        # Instructions for using UniqueConstraint and CheckConstraint from:
        # https://adamj.eu/tech/2021/02/26/django-check-constraints-prevent-self-following/
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["owner", "followed"],
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_follow",
                check=~models.Q(owner=models.F("followed")),
            ),
        ]

    def __str__(self):
        return f"{self.owner} follows {self.followed}"
