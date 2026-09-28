from django.contrib import admin

from .models import Badge, UserBadge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ["code", "name_uz", "icon", "sort_order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["code", "name_uz", "name_ru", "name_en"]
    list_editable = ["icon", "sort_order", "is_active"]


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ["user", "badge", "earned_at"]
    search_fields = ["user__username", "badge__code", "badge__name_uz"]
    date_hierarchy = "earned_at"