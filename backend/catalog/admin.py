from django.contrib import admin

from .models import Subject, Subtopic, Topic


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 0
    fields = ("name_uz", "slug", "sort_order", "is_active")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "code", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    prepopulated_fields = {"slug": ("name_uz",)}
    inlines = [TopicInline]
    search_fields = ("name_uz", "name_ru", "name_en")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "subject", "sort_order", "is_active")
    list_filter = ("subject", "is_active")
    search_fields = ("name_uz", "name_ru", "name_en")


@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "topic", "sort_order", "is_active")
    list_filter = ("topic__subject", "is_active")