"""Telegram bildirishnomalar uchun yordamchi xizmatlar.

Bot token/chat id env orqali sozlanadi (TELEGRAM_BOT_TOKEN,
TELEGRAM_CHAT_ID, TELEGRAM_ALLOWED_CHAT_IDS). Sozlanmagan bo'lsa barcha
chaqiruvlar hech narsa qilmaydi — rivojlanayotganda bloklanmaydi.
"""

import json
import logging
import time
from datetime import datetime, time
from html import escape as html_escape
from urllib import error as urlerror
from urllib import request as urllib_request

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

_API = "https://api.telegram.org/bot{token}/{method}"
_MAX_ATTEMPTS = 3


def get_bot_token():
    return getattr(settings, "TELEGRAM_BOT_TOKEN", "") or ""


def get_chat_ids():
    ids = list(getattr(settings, "TELEGRAM_ALLOWED_CHAT_IDS", []) or [])
    single = getattr(settings, "TELEGRAM_CHAT_ID", "") or ""
    if single and str(single) not in ids:
        ids.append(str(single))
    return ids


def is_configured():
    return bool(get_bot_token() and get_chat_ids())


def _call(method, payload):
    token = get_bot_token()
    if not token:
        return None
    url = _API.format(token=token, method=method)
    data = json.dumps(payload).encode("utf-8")
    req = urllib_request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    last_error = None
    for attempt in range(_MAX_ATTEMPTS):
        try:
            with urllib_request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urlerror.URLError, OSError, ValueError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < _MAX_ATTEMPTS - 1:
                time.sleep(1.5 * (attempt + 1))
    logger.warning(
        "Telegram API (%s) %s urinishdan keyin muvaffaqiyatsiz: %s",
        method,
        _MAX_ATTEMPTS,
        last_error,
    )
    return None


def send_message(text, parse_mode="HTML", silent=False):
    """Barcha sozlangan chatlarga xabar yuboradi. Javoblar ro'yxatini qaytaradi."""
    if not is_configured():
        return []
    results = []
    for chat_id in get_chat_ids():
        results.append(
            _call(
                "sendMessage",
                {
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": parse_mode,
                    "disable_web_page_preview": True,
                    "disable_notification": silent,
                },
            )
        )
    return results


def new_user_text(user):
    return (
        "<b>\U0001f389 Yangi foydalanuvchi ro'yxatdan o'tdi</b>\n\n"
        f"\U0001f464 Username: <code>{html_escape(user.username)}</code>\n"
        f"\U0001f3c5 Rol: {html_escape(user.get_role_display())}\n"
        f"\U0001f550 {timezone.localtime(user.date_joined):%d.%m.%Y %H:%M}"
    )


def question_submitted_text(question):
    author = question.created_by
    subject = question.subject.name_uz if question.subject_id else "—"
    snippet = (question.text_uz or "").strip().replace("\n", " ")[:120]
    author_name = author.get_full_name() if author else "—"
    if not author_name.strip():
        author_name = author.username if author else "—"
    return (
        "<b>\U0001f9d1\u200d\U0001f4bb O'qituvchi yangi savol qo'shdi</b>\n\n"
        f"\U0001f4da Fan: <b>{html_escape(subject)}</b>\n"
        f"\U0001f4dd Savol: {html_escape(snippet) or '—'}\n"
        f"\U0001f464 Muallif: {html_escape(author_name)}\n"
        f"\U0001f550 {timezone.localtime(question.created_at):%d.%m.%Y %H:%M}\n"
        "\u23f3 Holati: tekshiruvda"
    )


def send_new_user(user):
    send_message(new_user_text(user))


def send_question_submitted(question):
    send_message(question_submitted_text(question))


def daily_stats_text():
    from django.contrib.auth import get_user_model

    from practice.models import PracticeAnswer, PracticeSession
    from questions.models import Question

    User = get_user_model()
    today = timezone.localdate()
    day_start = timezone.make_aware(
        datetime.combine(today, time.min), timezone.get_current_timezone()
    )
    day_end = day_start + timezone.timedelta(days=1)

    total_users = User.objects.count()
    users_today = User.objects.filter(
        date_joined__gte=day_start, date_joined__lt=day_end
    ).count()
    total_questions = Question.objects.count()
    published = Question.objects.filter(status=Question.Status.PUBLISHED).count()
    pending = Question.objects.filter(status=Question.Status.DRAFT).count()
    sessions_today = PracticeSession.objects.filter(
        started_at__gte=day_start, started_at__lt=day_end
    ).count()
    answers_today = PracticeAnswer.objects.filter(
        answered_at__gte=day_start, answered_at__lt=day_end
    ).count()
    correct_today = PracticeAnswer.objects.filter(
        answered_at__gte=day_start,
        answered_at__lt=day_end,
        is_correct=True,
    ).count()
    accuracy = (
        round((correct_today / answers_today) * 100) if answers_today else None
    )
    accuracy_text = f"{accuracy}%" if accuracy is not None else "—"

    return (
        "<b>\U0001f4ca Abiturend — statistika</b>\n"
        f"\U0001f5d3\ufe0f {today:%d.%m.%Y}\n\n"
        f"\U0001f465 Jami foydalanuvchilar: <b>{total_users}</b>\n"
        f"\U0001f195 Bugun ro'yxatdan o'tganlar: <b>{users_today}</b>\n"
        f"\U0001f4dd Jami savollar: <b>{total_questions}</b>\n"
        f"\U0001f4cc Chop etilgan: <b>{published}</b>\n"
        f"\u23f3 Tekshiruvda: <b>{pending}</b>\n\n"
        f"\U0001f4c8 Bugungi faollik:\n"
        f"\u2022 Sessiyalar: <b>{sessions_today}</b>\n"
        f"\u2022 Javoblar: <b>{answers_today}</b>\n"
        f"\u2022 To'g'riligi: <b>{accuracy_text}</b>"
    )


def send_daily_stats():
    send_message(daily_stats_text())


WELCOME_TEXT = (
    "<b>\U0001f916 Abiturend bot</b>\n\n"
    "Quyidagi buyruqlar mavjud:\n"
    "/stats — platforma statistika xabarnomasi\n"
    "/start — bu xabarni ko'rsatish"
)