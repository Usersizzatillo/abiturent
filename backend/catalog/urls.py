from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SubjectViewSet, TopicViewSet

router = SimpleRouter()
router.register("subjects", SubjectViewSet, basename="subject")
router.register("topics", TopicViewSet, basename="topic")

urlpatterns = [
    path("", include(router.urls)),
]