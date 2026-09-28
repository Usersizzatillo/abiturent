from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from questions.importexport import FIELDS, import_csv

User = get_user_model()


class Command(BaseCommand):
    help = "CSV dan savollarni ommaviy import qiladi."

    def add_arguments(self, parser):
        parser.add_argument("path", help="CSV fayl yo'li")
        parser.add_argument(
            "--create-missing",
            action="store_true",
            help="Noma'lum fan/mavzuni avtomatik yaratadi.",
        )
        parser.add_argument(
            "--user",
            default="",
            help="Savol muallifi (username). Bo'sh bo'lsa created_by=None.",
        )

    def handle(self, *args, **options):
        path = options["path"]
        created_by = None
        if options["user"]:
            try:
                created_by = User.objects.get(username=options["user"])
            except User.DoesNotExist:
                raise CommandError(f"Foydalanuvchi topilmadi: {options['user']}")

        with open(path, encoding="utf-8-sig", newline="") as stream:
            created, errors = import_csv(
                stream, created_by=created_by, create_missing=options["create_missing"]
            )

        self.stdout.write(self.style.SUCCESS(f"Import yakunlandi: {created} ta savol yaratildi."))
        if errors:
            self.stderr.write(self.style.ERROR(f"Xatolar ({len(errors)} ta):"))
            for err in errors[:30]:
                self.stderr.write(self.style.ERROR("  - " + err))
            if len(errors) > 30:
                self.stderr.write(self.style.ERROR(f"  … va yana {len(errors) - 30} ta"))