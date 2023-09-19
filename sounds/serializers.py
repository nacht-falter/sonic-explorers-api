from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime
from datetime import timedelta
from rest_framework import serializers
from .models import Sound
from likes.models import Like
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryException
from tagulous.contrib.drf import TagSerializer


class AudioUploadField(serializers.FileField):
    """Custom serializer field for uploading audio files to Cloudinary. This is
    necessary because Cloudinary does not accept audio files from the default
    FileField, but the serializer does not recognize the CloudinaryField.

    Instructions for custom serializer fields from:
    https://www.django-rest-framework.org/api-guide/fields/#custom-fields

    Instructions for uploading audio files to Cloudinary from:
    https://cloudinary.com/documentation/django_image_and_video_upload

    Instructions for using Cloudinary transformations from:
    https://cloudinary.com/documentation/django_video_manipulation
    """

    def to_internal_value(self, data):
        try:
            uploaded_data = upload(
                data,
                resource_type="",
                folder="audio/",
                format="mp3",
                transformation=[
                    {"start_offset": 0, "end_offset": 30},
                ],
            )
            return uploaded_data["secure_url"]
        except CloudinaryException as e:
            raise serializers.ValidationError({"detail": e})


class SoundSerializer(TagSerializer, serializers.ModelSerializer):
    """Serializer for Sound model. Includes methods for formatting dates
    and for returning if the user is the owner of the sound.
    Also includes custom field for uploading audio files to Cloudinary as
    well as fields for counting likes and comments.

    Instructions for django-tagulous TagSerializer from:
    https://django-tagulous.readthedocs.io/en/latest/usage.html#django-rest-framework
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_avatar = serializers.ReadOnlyField(
        source="owner.profile.avatar.url"
    )
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    audio_file = AudioUploadField()
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    tags_count = serializers.IntegerField(read_only=True)

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

    def get_like_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, sound=obj).first()
            return like.id if like else None
        return None

    class Meta:
        model = Sound
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "audio_file",
            "tags",
            "image",
            "latitude",
            "longitude",
            "profile_id",
            "profile_avatar",
            "is_owner",
            "created_at",
            "updated_at",
            "like_id",
            "likes_count",
            "comments_count",
            "tags_count",
        ]


class SoundDetailSerializer(SoundSerializer):
    """Serializer for Sound update view. Makes required fields optional
    for PUT requests."""

    audio_file = AudioUploadField(required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""

    class Meta:
        model = Sound.tags.tag_model
        fields = ["name", "sound_set"]
