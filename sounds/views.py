from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters import rest_framework as drf_filters
from sonic_explorers_api.permissions import IsOwnerOrReadOnly
from .models import Sound
from profiles.models import Profile
from .serializers import SoundSerializer, SoundDetailSerializer, TagSerializer


class SoundFilter(drf_filters.FilterSet):
    """Custom filter for sound list view. Provides filtering options to
    display sounds from profiles followed by a user, sounds liked by a user,
    and sounds owned by a user.

    Instructions from django-filter docs:
    https://django-filter.readthedocs.io/en/main/guide/rest_framework.html
    """

    sounds_by_following = drf_filters.ModelChoiceFilter(
        queryset=Profile.objects.all(),
        field_name="owner__followed_by__owner__profile",
        label="Show sounds from profiles followed by:",
    )

    sounds_by_liked = drf_filters.ModelChoiceFilter(
        queryset=Profile.objects.all(),
        field_name="likes__owner__profile",
        label="Show sounds liked by:",
    )

    sounds_by_user = drf_filters.ModelChoiceFilter(
        queryset=Profile.objects.all(),
        field_name="owner__profile",
        label="Show sounds owned by:",
    )

    sounds_by_tag = drf_filters.ModelChoiceFilter(
        queryset=Sound.tags.tag_model.objects.all(),
        field_name="tags__name",
        label="Show sounds with tag:",
    )

    class Meta:
        model = Sound
        fields = [
            "sounds_by_following",
            "sounds_by_liked",
            "sounds_by_user",
            "sounds_by_tag",
        ]


class SoundList(generics.ListCreateAPIView):
    """Lists all sounds or creates a new sound. Provides options for
    filtering, searching, and sorting sounds
    """

    queryset = Sound.objects.annotate(
        likes_count=Count("likes", distinct=True),
        comments_count=Count("comments", distinct=True),
        tags_count=Count("tags", distinct=True),
    ).order_by("-created_at")
    serializer_class = SoundSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        drf_filters.DjangoFilterBackend,
    ]
    filterset_class = SoundFilter
    search_fields = [
        "owner__username",
        "title",
        "description",
        "tags__name",
    ]
    ordering_fields = [
        "likes_count",
        "comments_count",
        "likes__created_at",
        "comments__created_at",
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SoundDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates, or deletes a sound."""

    queryset = Sound.objects.annotate(
        likes_count=Count("likes", distinct=True),
        comments_count=Count("comments", distinct=True),
        tags_count=Count("tags", distinct=True),
    ).order_by("-created_at")
    serializer_class = SoundDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]


class TagList(generics.ListAPIView):
    """Lists all tags."""

    queryset = Sound.tags.tag_model.objects.all()
    serializer_class = TagSerializer


class TagDetail(generics.RetrieveAPIView):
    """Retrieves a tag."""

    queryset = Sound.tags.tag_model.objects.all()
    serializer_class = TagSerializer
