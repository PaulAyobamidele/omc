from django.urls import path
from .views import (
    SchoolClassListCreateView,
    SchoolClassRetrieveUpdateDestroyView,
    ClassSubjectListCreateView,
    ClassSubjectRetrieveUpdateDestroyView,
    AssignClassSubjectPermissionView,
)

urlpatterns = [
    path('school-classes/', SchoolClassListCreateView.as_view(), name='schoolclass-list-create'),
    path('school-classes/<int:pk>/', SchoolClassRetrieveUpdateDestroyView.as_view(), name='schoolclass-detail'),
    path('class-subjects/', ClassSubjectListCreateView.as_view(), name='classsubject-list-create'),
    path('class-subjects/<int:pk>/', ClassSubjectRetrieveUpdateDestroyView.as_view(), name='classsubject-detail'),
    path('permissions/assign/', AssignClassSubjectPermissionView.as_view(), name='assign-classsubject-permission'),
]
