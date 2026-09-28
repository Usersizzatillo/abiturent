from django.urls import path

from .views import PlanListView, SubscribeView, SubscriptionView

urlpatterns = [
    path("plans/", PlanListView.as_view(), name="premium-plans"),
    path("subscription/", SubscriptionView.as_view(), name="premium-subscription"),
    path("subscribe/", SubscribeView.as_view(), name="premium-subscribe"),
]