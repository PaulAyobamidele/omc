from django.urls import path

from .views import SignUpView
from .views import MeView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('me/', MeView.as_view(), name='me'),
]
