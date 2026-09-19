from django.urls import include, path

from .views import health

urlpatterns = [
    path("", health, name="health"),
    path("api/", include("core.api_urls")),
]