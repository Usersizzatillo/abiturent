from django.contrib import admin
from django.urls import include, path

from telegrambot.webhook import telegram_webhook

urlpatterns = [
    path("admin/", admin.site.urls),
    path("webhooks/telegram/", telegram_webhook, name="telegram-webhook"),
    path("", include("core.urls")),
]