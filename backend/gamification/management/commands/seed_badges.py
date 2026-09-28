from django.core.management.base import BaseCommand

from gamification.models import Badge

BADGES = [
    {
        "code": "first-steps",
        "name_uz": "Birinchi qadam",
        "name_ru": "Первый шаг",
        "name_en": "First steps",
        "description_uz": "Birinchi mashq sessiyasini yakunlang.",
        "description_ru": "Завершите первую тренировочную сессию.",
        "description_en": "Finish your first practice session.",
        "icon": "footprints",
        "sort_order": 1,
    },
    {
        "code": "regular",
        "name_uz": "Muntazam",
        "name_ru": "Постоянный",
        "name_en": "Regular",
        "description_uz": "10 ta sessiyani yakunlang.",
        "description_ru": "Завершите 10 сессий.",
        "description_en": "Finish 10 sessions.",
        "icon": "repeat",
        "sort_order": 2,
    },
    {
        "code": "marathoner",
        "name_uz": "Marafonchi",
        "name_ru": "Марафонец",
        "name_en": "Marathoner",
        "description_uz": "50 ta sessiyani yakunlang.",
        "description_ru": "Завершите 50 сессий.",
        "description_en": "Finish 50 sessions.",
        "icon": "trophy",
        "sort_order": 3,
    },
    {
        "code": "streak-3",
        "name_uz": "3 kunlik seriya",
        "name_ru": "Серия 3 дня",
        "name_en": "3-day streak",
        "description_uz": "3 kun ketma-ket mashq qiling.",
        "description_ru": "Занимайтесь 3 дня подряд.",
        "description_en": "Practice 3 days in a row.",
        "icon": "flame",
        "sort_order": 4,
    },
    {
        "code": "streak-7",
        "name_uz": "7 kunlik seriya",
        "name_ru": "Серия 7 дней",
        "name_en": "7-day streak",
        "description_uz": "7 kun ketma-ket mashq qiling.",
        "description_ru": "Занимайтесь 7 дней подряд.",
        "description_en": "Practice 7 days in a row.",
        "icon": "fire",
        "sort_order": 5,
    },
    {
        "code": "streak-30",
        "name_uz": "Oylik seriya",
        "name_ru": "Месячная серия",
        "name_en": "Monthly streak",
        "description_uz": "30 kun ketma-ket mashq qiling.",
        "description_ru": "Занимайтесь 30 дней подряд.",
        "description_en": "Practice 30 days in a row.",
        "icon": "crown",
        "sort_order": 6,
    },
    {
        "code": "sharp-shooter",
        "name_uz": "Aniq o'qchi",
        "name_ru": "Меткий стрелок",
        "name_en": "Sharp shooter",
        "description_uz": "Kamida 20 ta javobda 90% aniqlikka erishing.",
        "description_ru": "Достигните 90% точности как минимум на 20 ответах.",
        "description_en": "Reach 90% accuracy on at least 20 answers.",
        "icon": "crosshair",
        "sort_order": 7,
    },
    {
        "code": "perfect-100",
        "name_uz": "Mukammal sessiya",
        "name_ru": "Идеальная сессия",
        "name_en": "Perfect session",
        "description_uz": "Har bir savolga to'g'ri javob bering.",
        "description_ru": "Ответьте правильно на каждый вопрос.",
        "description_en": "Answer every question correctly.",
        "icon": "star",
        "sort_order": 8,
    },
    {
        "code": "centurion",
        "name_uz": "Yuzlarchi",
        "name_ru": "Сотник",
        "name_en": "Centurion",
        "description_uz": "Jami 100 ta savolga javob bering.",
        "description_ru": "Ответьте в сумме на 100 вопросов.",
        "description_en": "Answer 100 questions in total.",
        "icon": "shield",
        "sort_order": 9,
    },
    {
        "code": "scholar-500",
        "name_uz": "Olim",
        "name_ru": "Учёный",
        "name_en": "Scholar",
        "description_uz": "Jami 500 ta savolga javob bering.",
        "description_ru": "Ответьте в сумме на 500 вопросов.",
        "description_en": "Answer 500 questions in total.",
        "icon": "graduation",
        "sort_order": 10,
    },
    {
        "code": "explorer",
        "name_uz": "Kashfiyotchi",
        "name_ru": "Исследователь",
        "name_en": "Explorer",
        "description_uz": "Kamida 5 ta fandan mashq qiling.",
        "description_ru": "Позанимайтесь как минимум по 5 предметам.",
        "description_en": "Practice at least 5 subjects.",
        "icon": "compass",
        "sort_order": 11,
    },
    {
        "code": "exam-pro",
        "name_uz": "Imtihon ustasi",
        "name_ru": "Мастер экзамена",
        "name_en": "Exam pro",
        "description_uz": "5 ta sinov imtihonini yakunlang.",
        "description_ru": "Завершите 5 пробных экзаменов.",
        "description_en": "Finish 5 mock exams.",
        "icon": "timer",
        "sort_order": 12,
    },
]


class Command(BaseCommand):
    help = "Bazadagi badge'larni yaratadi (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for badge in BADGES:
            data = dict(badge)
            code = data.pop("code")
            _, ok = Badge.objects.get_or_create(code=code, defaults=data)
            if ok:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Yaratildi: {code}"))
        self.stdout.write(self.style.MIGRATE_HEADING(f"Jami yangi badge'lar: {created}"))
        if not created:
            self.stdout.write("Hammasi allaqachon mavjud.")