from django.urls import path
from . import views

urlpatterns = [
    path("sounds/", views.SoundList.as_view(), name="sounds"),
    path("sounds/<int:pk>", views.SoundDetail.as_view(), name="sound_detail"),
    path("tags/", views.TagList.as_view(), name="tags"),
    path("tags/<int:pk>", views.TagDetail.as_view(), name="tag_detail"),
]
