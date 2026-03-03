from django.urls import path
from .views import ParentDashboardView, ParentListView

urlpatterns = [
    path("dashboard/", ParentDashboardView.as_view(), name="parent-dashboard"),
    path("", ParentListView.as_view(), name="parent-list"),
]