from django.urls import path
from .views import SubjectListView, SubjectDetailView, AssignTeacherToSubjectView

urlpatterns = [
    path('', SubjectListView.as_view(), name='subject-list'),
    path('<int:pk>/', SubjectDetailView.as_view(), name='subject-detail'),
    path('assign-teacher/', AssignTeacherToSubjectView.as_view(), name='assign-teacher-subject'),
]
