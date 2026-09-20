"""Uptime monitoring: sayt + API holatini tekshiradi, buzilsa Telegramga ogohlantiradi.

Cron: */5 * * * * cd /opt/abiturend && \
  docker compose exec -T backend python manage.py tg_monitor
"""

import logging
from urllib import error as urlerror
from urllib import request as urllib_request

from django.conf import settings
from django.core.management.base import BaseCommand

from telegrambot.services import send_message

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sayt va API uptime'ni tekshiradi; nosozlik bo'lsa Telegramga xabar beradi."

    def _probe(self, url, timeout=15):
        try:
            with urllib_request.urlopen(url, timeout=timeout) as resp:
                return resp.status, resp.read(200).decode("utf-8", "replace")
        except urlerror.HTTPError as exc:
            return exc.code, ""
        except (urlerror.URLError, OSError, ValueError) as exc:
            return None, str(exc)

    def handle(self, *args, **options):
        allowed = getattr(settings, "ALLOWED_HOSTS", [])
        host = getattr(settings, "TELEGRAM_WEBHOOK_HOST", "") or ""
        if not host:
            host = next((h for h in allowed if "." in h and h != "localhost"), "")
        if not host:
            self.stderr.write("Domen aniqlanmadi (ALLOWED_HOSTS / TELEGRAM_WEBHOOK_HOST).")
            return

        base = f"https://{host}"
        results = []
        for label, url in (("sayt", f"{base}/uz"), ("api", f"{base}/api/health/")):
            status, body = self._probe(url)
            ok = status is not None and 200 <= status < 500
            results.append((label, url, status, ok, body))
            self.stdout.write(f"{label}: {status}")

        failures = [
            (label, url, status, body)
            for label, url, status, ok, body in results
            if not ok
        ]
        if not failures:
            self.stdout.write(self.style.SUCCESS("Barcha tekshiruvlar muvaffaqiyatli."))
            return

        lines = ["<b>❌ Abiturend monitoring: nosozlik</b>\n"]
        for label, url, status, body in failures:
            lines.append(f"• {label}: <code>{url}</code>")
            lines.append(f"  Holat: {status or 'bog'lanib bo'lmadi'}")
            if status == 500 and body:
                lines.append(f"  Javob: <code>{body[:120]}</code>")
        send_message("\n".join(lines))
        self.stderr.write("Nosozlik Telegramga yuborildi.")