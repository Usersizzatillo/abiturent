"""Telegram webhook endpoint.

Telegram yangi yangilanishlarni POST sifatida shu endpointga yuboradi.
Xavfsizlik: `X-Telegram-Bot-Api-Secret-Token` header'i bilan himoyalangan
(TELEGRAM_WEBHOOK_SECRET env). Webhook ro'yxatdan o'tkazish:
`python manage.py tg_set_webhook --drop` (yoki deploy paytida avtomatik).
"""

import hashlib
import hmac
import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import services

logger = logging.getLogger(__name__)


def _secret_ok(request) -> bool:
    secret = getattr(settings, "TELEGRAM_WEBHOOK_SECRET", "") or ""
    if not secret:
        return True
    header = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "") or ""
    return hmac.compare_digest(header.encode(), secret.encode())


def _handle_update(update):
    message = update.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = str(chat.get("id", ""))
    if chat_id not in services.get_chat_ids():
        return
    text = str(message.get("text") or "").strip()
    if not text:
        return

    if text == "/start":
        services.send_message(services.WELCOME_TEXT, chat_id=chat_id)
    elif text == "/help":
        services.send_message(services.HELP_TEXT, chat_id=chat_id)
    elif text == "/stats":
        services.send_message(services.daily_stats_text(), chat_id=chat_id)
    elif text == "/trend":
        services.send_message(services.daily_trend_text(), chat_id=chat_id)
    elif text == "/id":
        services.send_message(
            f"<b>Chat ID</b>: <code>{chat_id}</code>", chat_id=chat_id
        )
    elif text.startswith("/") and len(text) > 1:
        services.send_message(
            "Noma'lum buyruq. /help bilan tanishing.", chat_id=chat_id
        )
    else:
        services.send_message(
            "Xabar qabul qilindi, rahmat! 📨", chat_id=chat_id
        )


@csrf_exempt
@require_POST
def telegram_webhook(request):
    if not _secret_ok(request):
        logger.warning("Telegram webhook: ruxsatsiz so'rov")
        return JsonResponse({"ok": False, "error": "unauthorized"}, status=401)
    try:
        update = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "bad payload"}, status=400)
    try:
        _handle_update(update)
    except Exception:
        logger.exception("Telegram webhook ishlov berish xatosi")
    return JsonResponse({"ok": True})