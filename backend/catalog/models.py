import uuid

from django.db import models
from django.utils.text import slugify

from core.models import ActiveManager, TimeStampedModel

_SLUG_MAX = 96


def _unique_slug(queryset, raw_name):
    """Build a slug that is guaranteed to be storable and unique.

    ``slugify`` returns an empty string for names it cannot transliterate (pure
    Cyrillic, emoji, ...). An empty slug violates nothing on its own but collides
    with the next empty slug through the unique constraint, which surfaced as an
    IntegrityError on save, and it also produces a dead URL.
    """
    base = slugify(raw_name or "")[:_SLUG_MAX] or uuid.uuid4().hex[:12]
    candidate = base
    suffix = 2
    while queryset.filter(slug=candidate).exists():
        candidate = f"{base[: _SLUG_MAX - 3]}-{suffix}"
        suffix += 1
    return candidate


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
            self.slug = _unique_slug(Subject.objects.all(), self.name_uz)
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
            # Slug uniqueness is scoped to the subject.
            siblings = (
                Topic.objects.filter(subject_id=self.subject_id)
                if self.subject_id
                else Topic.objects.none()
            )
            self.slug = _unique_slug(siblings, self.name_uz)
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