from django.urls import path
from .views import CreateStudentView, StudentListView, StudentsByClassView

urlpatterns = [
    path("create/", CreateStudentView.as_view(), name="create-student"),
    path("", StudentListView.as_view(), name="student-list"),
    path("by-class/<int:class_id>/", StudentsByClassView.as_view(), name="students-by-class"),
]