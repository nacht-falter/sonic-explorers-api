from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    """Custom serializer to make the current user's profile id and avatar
    available on the API endpoint for the current user.
    Instructions from the CI DRF Walkthrough project.
    """

    profile_id = serializers.ReadOnlyField(source="profile.id")
    profile_avatar = serializers.ReadOnlyField(source="profile.avatar.url")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "profile_id",
            "profile_avatar",
        )
