from rest_framework import generics, permissions, filters
from django_filters import rest_framework as drf_filters
from sonic_explorers_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from sounds.models import Sound
from .serializers import CommentSerializer, CommentDetailSerializer


class CommentFilter(drf_filters.FilterSet):
    """Custom filter for comment list view. Provides filtering options to
    filter comments by sound.

    Instructions from django-filter docs:
    https://django-filter.readthedocs.io/en/main/guide/rest_framework.html
    """

    queryset = Sound.objects.all()

    comments_by_sound = drf_filters.ModelChoiceFilter(
        queryset=queryset,
        field_name="sound",
        label="Show comments for sound:",
    )

    class Meta:
        model = Comment
        fields = ["comments_by_sound"]


class CommentList(generics.ListCreateAPIView):
    """List comments or create a new one if user is logged in."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter,
        drf_filters.DjangoFilterBackend,
    ]
    ordering_fields = ["created_at", "updated_at"]
    filterset_class = CommentFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve a comment. Update or delete comments if user is owner."""

    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
