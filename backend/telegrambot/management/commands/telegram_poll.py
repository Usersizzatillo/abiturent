import json
import logging
import time
from urllib import error as urlerror
from urllib import request as urllib_request

from django.core.management.base import BaseCommand

from telegrambot.services import (
    get_bot_token,
    get_chat_ids,
    is_configured,
)
from telegrambot.webhook import _handle_command

logger = logging.getLogger(__name__)

_API = "https://api.telegram.org/bot{token}/{method}"


class Command(BaseCommand):
    help = "Telegram botni uzluksiz ishga tushiradi (getUpdates polling)."

    def handle(self, *args, **options):
        if not is_configured():
            self.stderr.write(
                "Telegram sozlanmagan (TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID)."
            )
            return
        self.chat_ids = get_chat_ids()
        self.stdout.write(
            self.style.SUCCESS("Bot ishga tushdi (Ctrl+C bilan to'xtatiladi)...")
        )
        self.stdout.flush()
        offset = None
        while True:
            try:
                data = self._get_updates(offset)
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    self._handle(update)
            except KeyboardInterrupt:
                self.stdout.write("\nTo'xtatildi.")
                self.stdout.flush()
                return
            except TimeoutError:
                logger.warning("Telegram polling vaqti tugadi, davom etiladi")
            except (urlerror.URLError, OSError, ValueError):
                logger.exception("Telegram polling xatosi")
                time.sleep(5)

    def _get_updates(self, offset):
        token = get_bot_token()
        url = _API.format(token=token, method="getUpdates")
        payload = {"timeout": 25, "allowed_updates": ["message", "callback_query"]}
        if offset is not None:
            payload["offset"] = offset
        data = json.dumps(payload).encode("utf-8")
        req = urllib_request.Request(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        with urllib_request.urlopen(req, timeout=40) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _handle(self, update):
        if "callback_query" in update:
            query = update["callback_query"]
            chat = (query.get("message") or {}).get("chat") or {}
            if str(chat.get("id", "")) in self.chat_ids:
                _handle_command(str(query.get("data") or ""), str(chat.get("id", "")))
                from telegrambot.services import answer_callback_query

                answer_callback_query(query.get("id", ""), "Ok ✅")
            return
        message = update.get("message") or {}
        chat = message.get("chat") or {}
        if str(chat.get("id", "")) not in self.chat_ids:
            return
        text = str(message.get("text") or "").strip()
        if text:
            _handle_command(text, str(chat.get("id", "")))