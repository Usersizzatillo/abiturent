from django.contrib import admin

from .models import PracticeAnswer, PracticeSession


class PracticeAnswerInline(admin.TabularInline):
    model = PracticeAnswer
    extra = 0
    fields = ("question", "selected_option", "is_correct", "answered_at")
    readonly_fields = ("question", "selected_option", "is_correct", "answered_at")
    can_delete = False


@admin.register(PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "subject",
        "mode",
        "status",
        "question_count",
        "progress_index",
        "correct_answers",
        "incorrect_answers",
        "started_at",
        "finished_at",
    )
    list_filter = ("mode", "status", "subject", "started_at")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    date_hierarchy = "started_at"
    readonly_fields = (
        "user",
        "subject",
        "topic",
        "mode",
        "status",
        "question_count",
        "progress_index",
        "correct_answers",
        "incorrect_answers",
        "started_at",
        "finished_at",
    )
    inlines = [PracticeAnswerInline]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(PracticeAnswer)
class PracticeAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "question", "is_correct", "answered_at")
    list_filter = ("is_correct", "answered_at", "session__subject")
    search_fields = ("session__user__username", "question__text_uz")
    readonly_fields = ("session", "question", "selected_option", "is_correct", "answered_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False