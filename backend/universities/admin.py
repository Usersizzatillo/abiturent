from django.contrib import admin

from .models import Direction, University


class DirectionInline(admin.TabularInline):
    model = Direction
    extra = 0
    show_change_link = True


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "city_uz", "established", "direction_count", "sort_order", "is_active")
    list_filter = ("is_active", "city_uz")
    search_fields = ("name_uz", "name_ru", "name_en")
    prepopulated_fields = {"slug": ("name_uz",)}
    inlines = [DirectionInline]

    @admin.display(description="Yo'nalishlar")
    def direction_count(self, obj):
        return obj.directions.count()


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "university", "code", "duration_years", "is_active")
    list_filter = ("is_active", "university")
    search_fields = ("name_uz", "name_ru", "name_en", "code")
    filter_horizontal = ("subjects",)