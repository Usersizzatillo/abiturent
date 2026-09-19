from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import QuestionViewSet

router = SimpleRouter()
router.register("questions", QuestionViewSet, basename="question")

urlpatterns = [
    path("", include(router.urls)),
]