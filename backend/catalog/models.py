from django.db import models
from django.utils.text import slugify

from core.models import ActiveManager, TimeStampedModel


class Subject(TimeStampedModel):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True, default="")
    name_en = models.CharField(max_length=255, blank=True, default="")
    slug = models.SlugField(max_length=128, unique=True, blank=True)
    code = models.CharField(max_length=32, blank=True, default="")
    icon = models.CharField(max_length=64, blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ["sort_order", "id"]
        db_table = "catalog_subject"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_uz or "")[:128]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz


class Topic(TimeStampedModel):
    subject = models.ForeignKey(
        Subject, related_name="topics", on_delete=models.CASCADE
    )
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True, default="")
    name_en = models.CharField(max_length=255, blank=True, default="")
    slug = models.SlugField(max_length=128, blank=True)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ["sort_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "slug"], name="uniq_topic_subject_slug"
            )
        ]
        db_table = "catalog_topic"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name_uz or "")[:96]
            self.slug = base
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz


class Subtopic(TimeStampedModel):
    topic = models.ForeignKey(
        Topic, related_name="subtopics", on_delete=models.CASCADE
    )
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True, default="")
    name_en = models.CharField(max_length=255, blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ["sort_order", "id"]
        db_table = "catalog_subtopic"

    def __str__(self):
        return self.name_uz