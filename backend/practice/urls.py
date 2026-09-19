from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .stats import StatsSummaryView
from .views import PracticeSessionViewSet

router = SimpleRouter()
router.register("sessions", PracticeSessionViewSet, basename="session")

urlpatterns = [
    path("", include(router.urls)),
    path("stats/summary/", StatsSummaryView.as_view(), name="stats-summary"),
]