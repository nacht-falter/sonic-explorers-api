from rest_framework import serializers
from .models import Profile
from follows.models import Follow


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model. Contains a method field to check if
    the user is the owner of the profile.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    follow_id = serializers.SerializerMethodField()
    sounds_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        return obj.owner == self.context["request"].user

    def get_follow_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            follow = Follow.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return follow.id if follow else None
        return None

    class Meta:
        model = Profile
        fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
            "display_name",
            "description",
            "avatar",
            "is_owner",
            "sounds_count",
            "followers_count",
            "following_count",
            "follow_id",
        ]
