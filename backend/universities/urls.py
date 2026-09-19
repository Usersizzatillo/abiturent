from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import DirectionViewSet, UniversityViewSet

router = SimpleRouter()
router.register("universities", UniversityViewSet, basename="university")
router.register("directions", DirectionViewSet, basename="direction")

urlpatterns = [
    path("", include(router.urls)),
]