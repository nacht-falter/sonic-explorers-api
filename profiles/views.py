from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from sonic_explorers_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """Lists all profiles. No create functionality, as profiles are created
    automatically, when a user is created (see signals.py)
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a profile. Restricted to the owner"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
