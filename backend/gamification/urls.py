from django.urls import path

from .views import BadgeCheckView, BadgeListView

urlpatterns = [
    path("badges/", BadgeListView.as_view(), name="gamification-badges"),
    path("badges/check/", BadgeCheckView.as_view(), name="gamification-check"),
]