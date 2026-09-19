import time

from django.core.management.base import BaseCommand

from catalog.models import Subject
from universities.models import Direction, University


def _subject(name_uz):
    try:
        return Subject.active.get(name_uz=name_uz)
    except Subject.DoesNotExist:
        return None


SEED = [
    {
        "name_uz": "Mirzo Ulug'bek nomidagi O'zbekiston Milliy universiteti",
        "name_ru": "Национальный университет Узбекистана имени Мирзо Улугбека",
        "name_en": "National University of Uzbekistan",
        "slug": "numu",
        "code": "NUU",
        "city_uz": "Toshkent",
        "city_ru": "Ташкент",
        "city_en": "Tashkent",
        "established": 1918,
        "website": "https://nuu.uz",
        "sort_order": 0,
        "directions": [
            {"name_uz": "Matematika", "code": "mat", "subjects": ["Matematika", "Fizika"], "duration_years": 4, "sort": 0},
            {"name_uz": "Fizika", "code": "fiz", "subjects": ["Fizika", "Matematika"], "duration_years": 4, "sort": 1},
            {"name_uz": "Biologiya", "code": "bio", "subjects": ["Biologiya", "Kimyo"], "duration_years": 4, "sort": 2},
        ],
    },
    {
        "name_uz": "Toshkent davlat texnika universiteti",
        "name_ru": "Ташкентский государственный технический университет",
        "name_en": "Tashkent State Technical University",
        "slug": "tdtu",
        "code": "TDTU",
        "city_uz": "Toshkent",
        "city_ru": "Ташкент",
        "city_en": "Tashkent",
        "established": 1928,
        "website": "https://tdtu.uz",
        "sort_order": 1,
        "directions": [
            {"name_uz": "Dasturiy injiniring", "code": "se", "subjects": ["Informatika", "Matematika"], "duration_years": 4, "sort": 0},
            {"name_uz": "Qurilish muhandisligi", "code": "civil", "subjects": ["Fizika", "Matematika"], "duration_years": 4, "sort": 1},
        ],
    },
    {
        "name_uz": "Samarqand davlat universiteti",
        "name_ru": "Самаркандский государственный университет",
        "name_en": "Samarkand State University",
        "slug": "samdu",
        "code": "SamDU",
        "city_uz": "Samarqand",
        "city_ru": "Самарканд",
        "city_en": "Samarkand",
        "established": 1927,
        "website": "https://samdu.uz",
        "sort_order": 2,
        "directions": [
            {"name_uz": "Matematika", "code": "mat", "subjects": ["Matematika", "Fizika"], "duration_years": 4, "sort": 0},
            {"name_uz": "O'zbek tili va adabiyoti", "code": "uzfil", "subjects": ["Ona tili va adabiyoti", "Tarix"], "duration_years": 4, "sort": 1},
        ],
    },
]


class Command(BaseCommand):
    help = "Universitet va yo'nalishlar bo'yicha minimal boshlang'ich ma'lumot yaratadi."

    def handle(self, *args, **options):
        for i, item in enumerate(SEED):
            uni, created = University.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "name_uz": item["name_uz"],
                    "name_ru": item["name_ru"],
                    "name_en": item["name_en"],
                    "code": item["code"],
                    "city_uz": item["city_uz"],
                    "city_ru": item["city_ru"],
                    "city_en": item["city_en"],
                    "established": item["established"],
                    "website": item["website"],
                    "sort_order": item["sort_order"],
                },
            )
            for d in item["directions"]:
                direction, _ = Direction.objects.get_or_create(
                    university=uni,
                    code=d["code"],
                    defaults={
                        "name_uz": d["name_uz"],
                        "duration_years": d["duration_years"],
                        "sort_order": d["sort"],
                    },
                )
                for name in d["subjects"]:
                    subject = _subject(name)
                    if subject and not direction.subjects.filter(id=subject.id).exists():
                        direction.subjects.add(subject)
            self.stdout.write(self.style.SUCCESS(f"[{i + 1}] {item['name_uz']} OK"))
        time.sleep(0)