from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model. Contains a method field to check if
    the user is the owner of the profile.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return obj.owner == self.context["request"].user

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
        ]
