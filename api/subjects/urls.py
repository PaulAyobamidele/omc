from django.urls import path
from .views import SubjectListCreateView, SubjectDetailView, AssignTeacherToSubjectView

urlpatterns = [
    path("", SubjectListCreateView.as_view(), name="subject-list-create"),
    path("<int:pk>/", SubjectDetailView.as_view(), name="subject-detail"),
    path("assign-teacher/", AssignTeacherToSubjectView.as_view(), name="assign-teacher-subject"),
]