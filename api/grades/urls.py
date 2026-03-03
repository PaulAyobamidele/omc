from django.urls import path
from .views import (
    GradeEntryCreateView,
    GradeEntryUpdateView,
    StudentGradesView,
    ParentGradesView,
    ClassGradesView,
    SubjectGradesView,
    StudentGradeSummaryView,
    ClassGradeSummaryView,
)

urlpatterns = [
    path("grades/enter/", GradeEntryCreateView.as_view(), name="grade-entry-create"),
    path("grades/<int:pk>/update/", GradeEntryUpdateView.as_view(), name="grade-entry-update"),
    path("grades/student/", StudentGradesView.as_view(), name="student-grades"),
    path("grades/parent/", ParentGradesView.as_view(), name="parent-grades"),
    path("grades/class/<int:class_id>/", ClassGradesView.as_view(), name="class-grades"),
    path("grades/subject/<int:subject_id>/", SubjectGradesView.as_view(), name="subject-grades"),
    path("grades/student/<int:student_id>/summary/", StudentGradeSummaryView.as_view(), name="student-summary"),
    path("grades/class/<int:class_id>/summary/", ClassGradeSummaryView.as_view(), name="class-summary"),
]
