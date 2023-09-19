from django.utils import timezone
from datetime import timedelta
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model. Includes methods for formatting
    created_at and updated_at fields for better readability and for
    checking if the user is the owner of the comment.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_avatar = serializers.ReadOnlyField(
        source="owner.profile.avatar.url"
    )
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return obj.owner == self.context["request"].user

    def get_created_at(self, obj):
        if obj.created_at > timezone.now() - timedelta(days=1):
            return naturaltime(obj.created_at)
        else:
            return obj.created_at.strftime("%d %b %Y, %I:%M %p")

    def get_updated_at(self, obj):
        if obj.updated_at > timezone.now() - timedelta(days=1):
            return naturaltime(obj.updated_at)
        else:
            return obj.updated_at.strftime("%d %b %Y, %I:%M %p")

    class Meta:
        model = Comment
        fields = [
            "id",
            "owner",
            "sound",
            "is_owner",
            "profile_id",
            "profile_avatar",
            "created_at",
            "updated_at",
            "content",
        ]


class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for CommentDetail view. Sets sound field to read only
    for updating comments.
    """

    sound = serializers.ReadOnlyField(source="sound.id")
