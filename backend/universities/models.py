from django.db import models
from django.utils.text import slugify

from catalog.models import Subject
from core.models import ActiveManager, TimeStampedModel


class University(TimeStampedModel):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True, default="")
    name_en = models.CharField(max_length=255, blank=True, default="")
    slug = models.SlugField(max_length=128, unique=True, blank=True)
    code = models.CharField(max_length=32, blank=True, default="")
    city_uz = models.CharField(max_length=128, blank=True, default="")
    city_ru = models.CharField(max_length=128, blank=True, default="")
    city_en = models.CharField(max_length=128, blank=True, default="")
    established = models.PositiveSmallIntegerField(null=True, blank=True)
    website = models.URLField(blank=True, default="")
    description_uz = models.TextField(blank=True, default="")
    description_ru = models.TextField(blank=True, default="")
    description_en = models.TextField(blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ["sort_order", "id"]
        db_table = "universities_university"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_uz or "")[:128]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz


class Direction(TimeStampedModel):
    university = models.ForeignKey(
        University, related_name="directions", on_delete=models.CASCADE
    )
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True, default="")
    name_en = models.CharField(max_length=255, blank=True, default="")
    code = models.CharField(max_length=32, blank=True, default="")
    subjects = models.ManyToManyField(
        Subject, related_name="directions", blank=True
    )
    duration_years = models.PositiveSmallIntegerField(null=True, blank=True)
    quota = models.PositiveIntegerField(null=True, blank=True)
    grant_places = models.PositiveIntegerField(null=True, blank=True)
    paid_places = models.PositiveIntegerField(null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ["sort_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["university", "code"], name="uniq_direction_university_code"
            )
        ]
        db_table = "universities_direction"

    def __str__(self):
        return f"{self.name_uz} — {self.university.name_uz}"