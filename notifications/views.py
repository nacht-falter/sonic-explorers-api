from rest_framework import generics, permissions
from sonic_explorers_api.permissions import IsNotificationOwner
from .models import Notification
from .serializers import NotificationSerializer


class NotificationList(generics.ListAPIView):
    """List a user's notifications. No create view, since notifications are
    automatically created.
    """

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NotificationDetail(generics.RetrieveDestroyAPIView):
    """Retrieve or delete a notification by id.
    Restricted to notification owner.
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotificationOwner]
