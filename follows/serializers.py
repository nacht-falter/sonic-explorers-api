from django.db import IntegrityError
from rest_framework import serializers
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for Follow model.
    The create method is overridden to prevent users from following the same
    user more than once.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    followed_name = serializers.ReadOnlyField(source="followed.username")

    class Meta:
        model = Follow
        fields = [
            "id",
            "owner",
            "followed",
            "followed_name",
            "created_at",
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            if "UNIQUE" in str(e):
                raise serializers.ValidationError(
                    {"detail": "You are already following this user."}
                )
            elif "CHECK" in str(e):
                raise serializers.ValidationError(
                    {"detail": "You cannot follow yourself."}
                )
            else:
                raise serializers.ValidationError(
                    {"detail": "Could not follow user. Please try again."}
                )
