from django.utils import timezone
from datetime import timedelta
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model. Includes method for formatting
    sent_at field for better readability.
    """
    owner = serializers.ReadOnlyField(source="owner.username")
    sender = serializers.ReadOnlyField(source="sender.username")
    sender_avatar = serializers.ReadOnlyField(
        source="sender.profile.avatar.url"
    )
    item_id = serializers.ReadOnlyField(source="item.id")
    title = serializers.ReadOnlyField(source="item.title")
    content = serializers.ReadOnlyField(source="item.content")
    sent_at = serializers.SerializerMethodField()


    def get_sent_at(self, obj):
        if obj.sent_at > timezone.now() - timedelta(days=1):
            return naturaltime(obj.sent_at)
        else:
            return obj.sent_at.strftime("%d %b %Y, %I:%M %p")

    class Meta:
        model = Notification
        fields = [
            "id",
            "owner",
            "sender",
            "sender_avatar",
            "sent_at",
            "item_id",
            "is_read",
            "title",
            "content",
        ]
