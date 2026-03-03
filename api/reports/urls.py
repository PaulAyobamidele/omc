from django.urls import path
from .views import StudentReportJSON

urlpatterns = [
    path("student/<int:student_id>/", StudentReportJSON.as_view(), name="student-report-json"),
]