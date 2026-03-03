from django.urls import path
from .views import SchoolRegisterView, SchoolPublicView, SchoolDetailView

urlpatterns = [
    path('register/', SchoolRegisterView.as_view(), name='school-register'),
    path('<slug:slug>/public/', SchoolPublicView.as_view(), name='school-public'),
    path('<slug:slug>/', SchoolDetailView.as_view(), name='school-detail'),
]
