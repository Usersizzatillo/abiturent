from django.contrib import admin

from .models import Question, QuestionOption


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 4
    fields = ("text_uz", "is_correct", "sort_order")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "topic", "difficulty", "status", "is_verified", "created_by")
    list_filter = ("subject", "difficulty", "status", "question_type", "is_verified", "is_official")
    search_fields = ("text_uz", "text_ru", "text_en")
    inlines = [QuestionOptionInline]
    prepopulated_fields = {}
    readonly_fields = ("created_at", "updated_at")