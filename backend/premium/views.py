from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscription, SubscriptionPlan
from .serializers import (
    ActivePlanSerializer,
    SubscribeSerializer,
    SubscriptionPlanSerializer,
)
from .services import active_subscription, remaining_sessions_today


class PlanListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        plans = SubscriptionPlan.objects.filter(is_active=True)
        return Response(SubscriptionPlanSerializer(plans, many=True).data)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sub = active_subscription(request.user)
        return Response(
            {
                "is_premium": sub is not None,
                "plan": ActivePlanSerializer(sub).data if sub else None,
                "remaining_sessions_today": remaining_sessions_today(request.user),
            }
        )


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = serializer.validated_data["plan_code"]

        active = active_subscription(request.user)
        now = timezone.now()
        if active is not None and active.ends_at and active.ends_at > now:
            starts_at = active.ends_at
        else:
            starts_at = now
        ends_at = starts_at + timedelta(days=plan.duration_days)

        # Real payment gateways would run here; for now activation is immediate
        # and idempotent: only the free tier can be taken without a gateway.
        if plan.tier == SubscriptionPlan.Tier.FREE or plan.price_uzs == 0:
            Subscription.objects.create(
                user=request.user, plan=plan, starts_at=starts_at, ends_at=ends_at
            )
        else:
            return Response(
                {
                    "detail": "To'lov tizimi hozircha faqat bepul tarif uchun ochiq.",
                    "plan_code": plan.code,
                    "price_uzs": plan.price_uzs,
                },
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )
        sub = active_subscription(request.user)
        return Response(
            {
                "is_premium": True,
                "plan": ActivePlanSerializer(sub).data if sub else None,
                "remaining_sessions_today": remaining_sessions_today(request.user),
            },
            status=status.HTTP_201_CREATED,
        )