from django.urls import path
from . import views


urlpatterns = [
    path("follows/", views.FollowList.as_view(), name="follows"),
    path(
        "follows/<int:pk>/", views.FollowDetail.as_view(), name="follow_detail"
    ),
]
