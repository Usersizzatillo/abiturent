from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "role", "phone", "is_active", "date_joined")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Platforma", {"fields": ("role", "phone", "avatar")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Platforma", {"fields": ("role", "phone")}),
    )