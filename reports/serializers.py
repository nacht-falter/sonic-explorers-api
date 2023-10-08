from django.utils import timezone
from datetime import timedelta
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Report model. Includes method for humanizing
    created_at field for better readability.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_avatar = serializers.ReadOnlyField(
        source="owner.profile.avatar.url"
    )
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        if obj.created_at > timezone.now() - timedelta(days=1):
            return naturaltime(obj.created_at)
        else:
            return obj.created_at.strftime("%d %b %Y, %I:%M %p")

    class Meta:
        model = Report
        fields = [
            "id",
            "owner",
            "sound",
            "profile_id",
            "profile_avatar",
            "created_at",
            "flag",
            "content",
            "review_status",
        ]
