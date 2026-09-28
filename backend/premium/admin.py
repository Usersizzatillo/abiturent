from django.contrib import admin

from .models import Subscription, SubscriptionPlan


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ["code", "tier", "name_uz", "price_uzs", "duration_days",
                    "max_sessions_per_day", "is_active", "sort_order"]
    list_filter = ["tier", "is_active"]
    search_fields = ["code", "name_uz", "name_ru", "name_en"]
    list_editable = ["is_active", "sort_order", "price_uzs"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "plan", "starts_at", "ends_at", "is_active", "created_at"]
    list_filter = ["plan", "created_at"]
    search_fields = ["user__username", "user__email"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"