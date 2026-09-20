from django.apps import AppConfig


class TelegrambotConfig(AppConfig):
    name = "telegrambot"

    def ready(self):
        from . import signals  # noqa: F401