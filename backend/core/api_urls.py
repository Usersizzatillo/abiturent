from django.urls import include, path

from .views import api_root, health

# Mounted under /api/
urlpatterns = [
    path("health/", health, name="api-health"),
    path("auth/", include("accounts.urls")),
    path("", include("catalog.urls")),
    path("", include("questions.urls")),
    path("", include("practice.urls")),
    path("", include("universities.urls")),
    path("", api_root, name="api-root"),
]