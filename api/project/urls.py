from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("api/schools/", include("schools.urls")),
    path("api/users/", include("users.urls")),
    path("api/subjects/", include("subjects.urls")),
    path("api/teachers/", include("teachers.urls")),
    path("api/parents/", include("parents.urls")),
    path("api/students/", include("students.urls")),
    path("api/classes/", include("classes.urls")),
    path("api/", include("grades.urls")),
    path("api/reports/", include("reports.urls")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)