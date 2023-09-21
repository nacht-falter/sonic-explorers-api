from django.urls import path
from . import views

urlpatterns = [
    path(
        "notifications/",
        views.NotificationList.as_view(),
        name="notifications",
    ),
    path(
        "notifications/<int:pk>",
        views.NotificationDetail.as_view(),
        name="notification_detail",
    ),
]
