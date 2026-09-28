from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Badge(TimeStampedModel):
    code = models.CharField(max_length=48, unique=True, db_index=True)
    name_uz = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120, blank=True, default="")
    name_en = models.CharField(max_length=120, blank=True, default="")
    description_uz = models.TextField(blank=True, default="")
    description_ru = models.TextField(blank=True, default="")
    description_en = models.TextField(blank=True, default="")
    icon = models.CharField(max_length=16, default="star")
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    objects = models.Manager()

    class Meta:
        ordering = ["sort_order", "id"]
        db_table = "gamification_badge"

    def __str__(self):
        return self.code


class UserBadge(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="gamification_badges", on_delete=models.CASCADE
    )
    badge = models.ForeignKey(
        Badge, related_name="earned_by", on_delete=models.CASCADE
    )
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-earned_at"]
        db_table = "gamification_user_badge"
        constraints = [
            models.UniqueConstraint(fields=["user", "badge"], name="uniq_user_badge")
        ]

    def __str__(self):
        return f"{self.user} earned {self.badge.code}"