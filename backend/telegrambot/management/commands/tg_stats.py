from django.core.management.base import BaseCommand

from telegrambot.services import daily_stats_text, send_message


class Command(BaseCommand):
    help = "Kunlik platforma statistikasini Telegramga yuboradi."

    def handle(self, *args, **options):
        results = send_message(daily_stats_text())
        ok = len([r for r in results if r])
        if not ok:
            self.stderr.write(
                "Statistika yuborilmadi (Telegram sozlanmagan yoki API xatosi)."
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Statistika {ok} ta chatga yuborildi.")
            )
        if len(results) - ok:
            self.stderr.write(f"{len(results) - ok} ta chatga yuborilmadi.")