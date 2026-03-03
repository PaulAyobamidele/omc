from django.urls import path
from .views import TeacherDashboardView, TeacherListView

urlpatterns = [
    path("dashboard/", TeacherDashboardView.as_view(), name="teacher-dashboard"),
    path("", TeacherListView.as_view(), name="teacher-list"),
]