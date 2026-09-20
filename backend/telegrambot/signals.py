import logging
import threading

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from questions.models import Question

from . import services

logger = logging.getLogger(__name__)

User = get_user_model()


def _fire(target, *args):
    if not services.is_configured():
        return
    threading.Thread(target=_safe, args=(target, *args), daemon=True).start()


def _safe(target, *args):
    try:
        target(*args)
    except Exception:
        logger.exception("Telegram bildirishnomasi yuborilmadi")


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        _fire(services.send_new_user, instance)


@receiver(post_save, sender=Question)
def question_created(sender, instance, created, **kwargs):
    if not created:
        return
    created_by = instance.created_by
    if created_by is None or getattr(created_by, "role", None) != User.Role.TEACHER:
        return
    _fire(services.send_question_submitted, instance)