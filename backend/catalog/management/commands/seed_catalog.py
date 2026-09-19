from django.core.management.base import BaseCommand

from catalog.models import Subject

SUBJECTS = [
    ("Matematika", "Математика", "Mathematics", "matematika", "M", "pi"),
    ("Ona tili va adabiyot", "Родной язык и литература", "Native language and literature", "ona-tili-va-adabiyot", "OTA", "book"),
    ("Ingliz tili", "Английский язык", "English language", "ingliz-tili", "ING", "globe"),
    ("Fizika", "Физика", "Physics", "fizika", "F", "atom"),
    ("Kimyo", "Химия", "Chemistry", "kimyo", "K", "flask"),
    ("Biologiya", "Биология", "Biology", "biologiya", "B", "leaf"),
    ("Tarix", "История", "History", "tarix", "T", "landmark"),
    ("Geografiya", "География", "Geography", "geografiya", "G", "map"),
    ("Rus tili", "Русский язык", "Russian language", "rus-tili", "R", "languages"),
    ("Informatika", "Информатика", "Informatics", "informatika", "INF", "cpu"),
    ("Tarbiya", "Воспитание", "Upbringing", "tarbiya", "TAR", "heart"),
    ("Jahon tarixi", "Всемирная история", "World history", "jahon-tarixi", "JT", "globe"),
    ("Ijtimoiy-iqtisodiy bilimlar", "Обществоведение", "Social and economic studies", "ijtimoiy-iqtisodiy-bilimlar", "iqt", "scale"),
]

LANG_FIELDS = {"uz": "name_uz", "ru": "name_ru", "en": "name_en"}


class Command(BaseCommand):
    help = "Seeds the default DTM subject catalog."

    def handle(self, *args, **options):
        created = 0
        for i, (uz, ru, en, slug, code, icon) in enumerate(SUBJECTS):
            _, was_created = Subject.objects.update_or_create(
                slug=slug,
                defaults={
                    "name_uz": uz,
                    "name_ru": ru,
                    "name_en": en,
                    "code": code,
                    "icon": icon,
                    "sort_order": i,
                    "is_active": True,
                },
            )
            created += 1 if was_created else 0
        self.stdout.write(
            self.style.SUCCESS(
                f"Subjects: {Subject.objects.count()} total ({created} new)."
            )
        )