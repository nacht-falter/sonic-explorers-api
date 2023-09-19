from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to restrict editing to the owner of an object"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsNotificationOwner(permissions.BasePermission):
    """Custom permission to restrict access to notifications to the owner of a
    notification."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        raise PermissionDenied(
            "403 Permission denied"
        )


class IsAdminOrCreateOnly(permissions.BasePermission):
    """Custom permission to restrict read access to admin users, while
    allowing create access to all users.

    Instructions for has_permission method from DRF docs:
    https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return request.user.is_staff
