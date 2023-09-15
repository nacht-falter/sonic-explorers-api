from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime
from datetime import timedelta
from rest_framework import serializers
from .models import Sound
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryException


class AudioUploadField(serializers.FileField):
    """Custom serializer field for uploading audio files to Cloudinary. This is
    necessary because Cloudinary does not accept audio files from the default
    FileField, but the serializer does not recognize the CloudinaryField.

    Instructions for custom serializer fields from:
    https://www.django-rest-framework.org/api-guide/fields/#custom-fields

    Instructions for uploading audio files to Cloudinary from:
    https://cloudinary.com/documentation/django_image_and_video_upload
    """

    def to_internal_value(self, data):
        try:
            uploaded_data = upload(
                data,
                resource_type="",
                folder="audio/",
            )
            return uploaded_data["secure_url"]
        except CloudinaryException as e:
            raise serializers.ValidationError(
                {"detail": e}
            )


class SoundSerializer(serializers.ModelSerializer):
    """Serializer for Sound model."""

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_avatar = serializers.ReadOnlyField(
        source="owner.profile.avatar.url"
    )
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    audio_file = AudioUploadField()

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
        model = Sound
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "audio_file",
            "image",
            "latitude",
            "longitude",
            "profile_id",
            "profile_avatar",
            "is_owner",
            "created_at",
            "updated_at",
        ]


class SoundDetailSerializer(SoundSerializer):
    """Serializer for Sound update view. Makes audio_file field optional."""

    audio_file = AudioUploadField(required=False)
