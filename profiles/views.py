from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters import rest_framework as drf_filters
from .models import Profile
from .serializers import ProfileSerializer
from sonic_explorers_api.permissions import IsOwnerOrReadOnly


class ProfileFilter(drf_filters.FilterSet):
    """Custom filter for profile list view. Provides filtering options to
    display a profiles followers and the users a profile owner is following.

    Instructions from django-filter docs:
    https://django-filter.readthedocs.io/en/main/guide/rest_framework.html
    """

    queryset = Profile.objects.all()

    following = drf_filters.ModelChoiceFilter(
        queryset=queryset,
        field_name="owner__followed_by__owner__profile",
        label="Show profiles followed by:",
    )
    followers = drf_filters.ModelChoiceFilter(
        queryset=queryset,
        field_name="owner__following__followed__profile",
        label="Show profiles following:",
    )

    class Meta:
        model = Profile
        fields = ["followers", "following"]


class ProfileList(generics.ListAPIView):
    """Lists all profiles. No create functionality, as profiles are created
    automatically, when a user is created (see signals.py). Provides
    filtering options by followers and following.
    """

    queryset = Profile.objects.annotate(
        sounds_count=Count("owner__sound", distinct=True),
        followers_count=Count("owner__followed_by", distinct=True),
        following_count=Count("owner__following", distinct=True),
    ).order_by("-created_at")
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, drf_filters.DjangoFilterBackend]
    filterset_class = ProfileFilter
    ordering_fields = [
        "sounds_count",
        "followers_count",
        "following_count",
        "owner__following__created_at",
        "owner__followed_by__created_at",
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """Retrieve, update, or delete a profile. Restricted to the owner"""

    queryset = Profile.objects.annotate(
        sounds_count=Count("owner__sound", distinct=True),
        followers_count=Count("owner__followed_by", distinct=True),
        following_count=Count("owner__following", distinct=True),
    ).order_by("-created_at")
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
