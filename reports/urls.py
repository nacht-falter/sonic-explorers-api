from django.urls import path
from . import views

urlpatterns = [
    path("reports/", views.ReportList.as_view(), name="reports"),
    path(
        "reports/<int:pk>",
        views.ReportDetail.as_view(),
        name="report_detail",
    ),
]
