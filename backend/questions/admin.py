from django.contrib import admin
from django.http import HttpResponse

from .importexport import export_csv
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
    actions = ["export_csv"]

    @admin.action(description="Tanlangan savollarni CSV ga eksport qilish")
    def export_csv(self, request, queryset):
        if not queryset.exists():
            self.message_user(request, "Tanlangan savollar yo'q.", level="warning")
            return
        csv_text = export_csv(queryset)
        response = HttpResponse(csv_text, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="questions.csv"'
        return response