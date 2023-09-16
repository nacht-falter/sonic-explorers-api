from rest_framework import generics, permissions
from .models import Sound
from .serializers import SoundSerializer, SoundDetailSerializer, TagSerializer
from sonic_explorers_api.permissions import IsOwnerOrReadOnly


class SoundList(generics.ListCreateAPIView):
    """Lists all sounds or creates a new sound."""

    queryset = Sound.objects.all()
    serializer_class = SoundSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SoundDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates, or deletes a sound."""

    queryset = Sound.objects.all()
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
