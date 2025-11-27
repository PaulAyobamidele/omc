from django.urls import path
from .views import GradeCreateView, StudentGradesView, ParentGradesView


urlpatterns = [
    path('grades/enter/', GradeCreateView.as_view(), name='grade-enter'),
    path('grades/', GradeCreateView.as_view(), name='grade-create'),
    path('grades/student/', StudentGradesView.as_view(), name='student-grades'),
    path('grades/parent/', ParentGradesView.as_view(), name='parent-grades'),
]

