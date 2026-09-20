from django.core.management.base import BaseCommand

from catalog.models import Subject
from questions.models import Question, QuestionOption


def _q(subject, text, opts, correct_idx, explanation, difficulty=2, qtype="single"):
    q = Question.objects.create(
        subject=subject,
        text_uz=text["uz"],
        text_ru=text.get("ru", ""),
        text_en=text.get("en", ""),
        question_type=qtype,
        difficulty=difficulty,
        explanation_uz=explanation.get("uz", ""),
        explanation_ru=explanation.get("ru", ""),
        explanation_en=explanation.get("en", ""),
        source_type=Question.SourceType.CUSTOM,
        is_official=False,
        is_verified=True,
        status=Question.Status.PUBLISHED,
    )
    for i, opt in enumerate(opts):
        QuestionOption.objects.create(
            question=q,
            text_uz=opt["uz"],
            text_ru=opt.get("ru", ""),
            text_en=opt.get("en", ""),
            is_correct=(i == correct_idx),
            sort_order=i,
        )
    return q


class Command(BaseCommand):
    help = "Seed published questions for core subjects."

    def handle(self, *args, **options):
        from .seed_data import BANK

        created = 0
        for slug, items in BANK.items():
            try:
                subject = Subject.objects.get(slug=slug)
            except Subject.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"skip subject {slug} (absent)"))
                continue
            existing = Question.objects.filter(status=Question.Status.PUBLISHED, subject=subject).count()
            if existing >= len(items):
                self.stdout.write(f"{slug}: already has {existing} questions, skip")
                continue
            for item in items:
                _q(
                    subject,
                    item["q"],
                    item["opts"],
                    item["correct"],
                    item.get("exp", {}),
                    item.get("diff", 2),
                )
                created += 1
            self.stdout.write(self.style.SUCCESS(f"{slug}: +{len(items)} questions"))
        self.stdout.write(self.style.SUCCESS(f"done. created={created}"))