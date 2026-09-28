from django.core.management.base import BaseCommand

from premium.models import SubscriptionPlan

PLANS = [
    {
        "code": "free-trial",
        "tier": SubscriptionPlan.Tier.FREE,
        "name_uz": "Bepul (sinov)",
        "name_ru": "Бесплатный (пробный)",
        "name_en": "Free (trial)",
        "description_uz": "Bepul tarif: kuniga 3 ta sessiya.",
        "description_ru": "Бесплатный тариф: 3 сессии в день.",
        "description_en": "Free tier: 3 sessions per day.",
        "price_uzs": 0,
        "duration_days": 30,
        "max_sessions_per_day": 3,
        "sort_order": 0,
    },
    {
        "code": "pro-monthly",
        "tier": SubscriptionPlan.Tier.PRO,
        "name_uz": "PRO — Oylik",
        "name_ru": "PRO — Месячный",
        "name_en": "PRO — Monthly",
        "description_uz": "Cheksiz sessiyalar, barcha fanlar va imtihonlar.",
        "description_ru": "Безлимитные сессии, все предметы и экзамены.",
        "description_en": "Unlimited sessions, all subjects and exams.",
        "price_uzs": 49_000,
        "duration_days": 30,
        "max_sessions_per_day": None,
        "sort_order": 1,
    },
]


class Command(BaseCommand):
    help = "Bazadagi premium tariflarini yaratadi (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for plan in PLANS:
            data = dict(plan)
            code = data.pop("code")
            _, ok = SubscriptionPlan.objects.get_or_create(code=code, defaults=data)
            if ok:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Yaratildi: {code}"))
        self.stdout.write(self.style.MIGRATE_HEADING(f"Jami yangi planlar: {created}"))
        if not created:
            self.stdout.write("Hammasi allaqachon mavjud.")