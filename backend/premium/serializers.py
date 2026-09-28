from rest_framework import serializers

from .models import Subscription, SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "code",
            "tier",
            "name_uz",
            "name_ru",
            "name_en",
            "description_uz",
            "description_ru",
            "description_en",
            "price_uzs",
            "duration_days",
            "max_sessions_per_day",
            "unlimited_sessions",
        ]


class ActivePlanSerializer(serializers.ModelSerializer):
    plan = serializers.CharField(source="plan.code")
    plan_name_uz = serializers.CharField(source="plan.name_uz")
    plan_name_ru = serializers.CharField(source="plan.name_ru")
    plan_name_en = serializers.CharField(source="plan.name_en")
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "id",
            "plan",
            "plan_name_uz",
            "plan_name_ru",
            "plan_name_en",
            "starts_at",
            "ends_at",
            "is_active",
        ]


class SubscribeSerializer(serializers.Serializer):
    plan_code = serializers.CharField()

    def validate_plan_code(self, value):
        try:
            return SubscriptionPlan.objects.get(code=value, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Bunday aktiv plan mavjud emas.")