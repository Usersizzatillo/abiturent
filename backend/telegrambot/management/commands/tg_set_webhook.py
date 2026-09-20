import json
from urllib import request as urllib_request

from django.conf import settings
from django.core.management.base import BaseCommand

from telegrambot.services import get_bot_token

_API = "https://api.telegram.org/bot{token}/{method}"


class Command(BaseCommand):
    help = "Telegram webhook'ni ro'yxatdan o'tkazadi (URL + secret token)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            default="",
            help="Webhook URL (odatda https://domen/webhooks/telegram/)",
        )
        parser.add_argument(
            "--drop",
            action="store_true",
            help="Oldingi webhook'ni bekor qilib, yangisini o'rnatadi",
        )

    def handle(self, *args, **options):
        token = get_bot_token()
        if not token:
            self.stderr.write("TELEGRAM_BOT_TOKEN sozlanmagan.")
            return
        secret = getattr(settings, "TELEGRAM_WEBHOOK_SECRET", "") or ""

        if options["drop"]:
            result = self._call(token, "deleteWebhook", {"drop_pending_updates": True})
            if result and result.get("ok"):
                self.stdout.write(self.style.SUCCESS("Webhook bekor qilindi."))
            else:
                self.stderr.write(f"deleteWebhook xatosi: {result}")
            return

        url = options["url"]
        if not url:
            host = getattr(settings, "TELEGRAM_WEBHOOK_HOST", "") or ""
            if not host:
                allowed = getattr(settings, "ALLOWED_HOSTS", [])
                host = next((h for h in allowed if "." in h and h != "localhost"), "")
            if not host:
                self.stderr.write("--url ko'rsating yoki domenni ALLOWED_HOSTS ga qo'ying.")
                return
            url = f"https://{host}/webhooks/telegram/"

        payload = {
            "url": url,
            "allowed_updates": ["message"],
            "drop_pending_updates": True,
        }
        if secret:
            payload["secret_token"] = secret
        result = self._call(token, "setWebhook", payload)
        if result and result.get("ok"):
            self.stdout.write(self.style.SUCCESS(f"Webhook o'rnatildi: {url}"))
        else:
            self.stderr.write(f"setWebhook xatosi: {result}")

    def _call(self, token, method, payload):
        req = urllib_request.Request(
            _API.format(token=token, method=method),
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib_request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))