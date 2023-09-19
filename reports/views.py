from rest_framework import generics, permissions, filters
from django_filters import rest_framework as drf_filters
from django.contrib.auth.models import User
from sonic_explorers_api.permissions import IsAdminOrCreateOnly
from .models import Report
from sounds.models import Sound
from .serializers import ReportSerializer


class ReportFilter(drf_filters.FilterSet):
    """Custom filter for  ReportList view. Provides filtering options to
    filter reports by sound, by user, or by flag.

    Instructions from django-filter docs:
    https://django-filter.readthedocs.io/en/main/guide/rest_framework.html
    """

    reports_by_sound = drf_filters.ModelChoiceFilter(
        queryset=Sound.objects.all(),
        field_name="sound",
        label="Show reports for sound:",
    )

    reports_by_user = drf_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name="owner",
        label="Show reports by user:",
    )

    reports_by_flag = drf_filters.ChoiceFilter(
        choices=Report.FLAG_CHOICES,
        field_name="flag",
        label="Show reports by flag:",
    )

    class Meta:
        model = Report
        fields = [
            "reports_by_sound",
            "reports_by_user",
            "reports_by_flag",
        ]


class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminOrCreateOnly]
    filter_backends = [filters.OrderingFilter, drf_filters.DjangoFilterBackend]
    filterset_class = ReportFilter
    ordering_fields = ["created_at", "flag"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReportDetail(generics.RetrieveDestroyAPIView):
    """Retrieve a report. Delete reports if user is admin."""

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAdminUser]
