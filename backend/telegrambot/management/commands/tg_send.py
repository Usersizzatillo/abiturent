from django.core.management.base import BaseCommand

from telegrambot.services import send_message


class Command(BaseCommand):
    help = "Telegram sozlangan chatlarga istalgan xabarni yuboradi."

    def add_arguments(self, parser):
        parser.add_argument("text", nargs="+", help="Yuboriladigan matn")
        parser.add_argument(
            "--silent", action="store_true", help="Ovozsiz xabar (bilintirishsiz)"
        )

    def handle(self, *args, **options):
        text = " ".join(options["text"])
        results = send_message(text, silent=options["silent"])
        ok = len([r for r in results if r])
        if not ok:
            self.stderr.write(
                "Xabar yuborilmadi (Telegram sozlanmagan yoki API xatosi)."
            )
        else:
            self.stdout.write(self.style.SUCCESS(f"Xabar {ok} ta chatga yuborildi."))
        if len(results) - ok:
            self.stderr.write(f"{len(results) - ok} ta chatga yuborilmadi.")