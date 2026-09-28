import sys

from django.core.management.base import BaseCommand

from questions.importexport import FIELDS, export_csv
from questions.models import Question


class Command(BaseCommand):
    help = "Savollar bazasini CSV formatida eksport qiladi."

    def add_arguments(self, parser):
        parser.add_argument(
            "--status",
            default="",
            help="Filtr: published|draft|archived (bo'sh bo'lsa hammasi)",
        )
        parser.add_argument(
            "--path",
            default="",
            help="Chiqish fayli. Berilmasa stdout ga yoziladi.",
        )

    def handle(self, *args, **options):
        queryset = Question.objects.select_related("subject", "topic")
        if options["status"]:
            queryset = queryset.filter(status=options["status"])

        text = export_csv(queryset)
        if options["path"]:
            with open(options["path"], "w", encoding="utf-8", newline="") as fh:
                fh.write(text)
            self.stdout.write(
                self.style.SUCCESS(
                    f"{queryset.count()} ta savol {options['path']} ga yozildi."
                )
            )
        else:
            sys.stdout.write(text)