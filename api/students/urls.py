# students/urls.py
from django.urls import path
from .views import CreateStudentView

urlpatterns = [
    path('students/create/', CreateStudentView.as_view(), name='create-student'),
]
