from django.urls import path
from .views import StudentReportJSON

urlpatterns = [
    path('student/<int:student_id>/json/', StudentReportJSON.as_view(), name='student-report-json'),
]
