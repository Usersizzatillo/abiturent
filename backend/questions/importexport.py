"""CSV import/export helpers for the question bank.

Format (first line is the header; ``option1..option6`` columns are optional,
up to six per question):

    subject,topic,text_uz,text_ru,text_en,question_type,difficulty,source_type,
    status,is_verified,explanation_uz,explanation_ru,explanation_en,
    option1_uz,option1_correct,option2_uz,option2_correct,...option6_correct

``subject`` is matched by slug first, then by localized name. With
``create_missing=True`` unknown subjects/topics are created on the fly.
"""

import csv
from io import StringIO

from catalog.models import Subject, Topic
from django.db import transaction
from django.utils.text import slugify

from .models import Question, QuestionOption

OPTION_COUNT = 6

FIELDS = [
    "subject",
    "topic",
    "text_uz",
    "text_ru",
    "text_en",
    "question_type",
    "difficulty",
    "source_type",
    "status",
    "is_verified",
    "explanation_uz",
    "explanation_ru",
    "explanation_en",
    *sum(
        ([f"option{n}_uz", f"option{n}_correct"] for n in range(1, OPTION_COUNT + 1)),
        [],
    ),
]


def _clean(value):
    if value is None:
        return ""
    return str(value).strip()


def _resolve_subject(raw, create_missing):
    raw = _clean(raw)
    if not raw:
        return None, "subject maydoni bo'sh"
    match = Subject.objects.filter(slug__iexact=raw).first()
    if match is None:
        match = (
            Subject.objects.filter(
                name_uz__iexact=raw,
            )
            .first()
            or Subject.objects.filter(name_ru__iexact=raw).first()
            or Subject.objects.filter(name_en__iexact=raw).first()
        )
    if match is None and create_missing:
        match = Subject.objects.create(
            name_uz=raw,
            slug=slugify(raw)[:50] or f"subject-{Subject.objects.count() + 1}",
        )
    if match is None:
        return None, f"Fan topilmadi: {raw}"
    return match, None


def _resolve_topic(subject, raw, create_missing):
    raw = _clean(raw)
    if not raw:
        return None
    match = Topic.objects.filter(subject=subject, slug__iexact=raw).first()
    if match is None:
        match = (
            Topic.objects.filter(subject=subject, name_uz__iexact=raw).first()
            or Topic.objects.filter(subject=subject, name_ru__iexact=raw).first()
            or Topic.objects.filter(subject=subject, name_en__iexact=raw).first()
        )
    if match is None and create_missing:
        match = Topic.objects.create(
            subject=subject,
            name_uz=raw,
            slug=slugify(raw)[:50] or f"topic-{Topic.objects.count() + 1}",
        )
    return match


def _read_options(row):
    options = []
    for n in range(1, OPTION_COUNT + 1):
        text = _clean(row.get(f"option{n}_uz", ""))
        if not text:
            continue
        correct_raw = _clean(row.get(f"option{n}_correct", ""))
        is_correct = correct_raw.lower() in {"1", "true", "yes", "on"}
        options.append(
            {
                "text_uz": text,
                "text_ru": _clean(row.get(f"option{n}_ru", "")),
                "text_en": _clean(row.get(f"option{n}_en", "")),
                "is_correct": is_correct,
            }
        )
    return options


def parse_rows(reader, created_by=None, create_missing=False):
    """Yield ``(question, error)`` tuples. Caller persists the questions."""
    for row_number, row in enumerate(reader, start=2):
        text_uz = _clean(row.get("text_uz", ""))
        if not text_uz:
            yield None, f"{row_number}-qator: text_uz bo'sh"
            continue

        subject, err = _resolve_subject(row.get("subject", ""), create_missing)
        if err:
            yield None, f"{row_number}-qator: {err}"
            continue

        options = _read_options(row)
        if len(options) < 2:
            yield None, f"{row_number}-qator: kamida 2 ta variant kerak"
            continue
        correct = [o for o in options if o["is_correct"]]
        if not correct:
            yield None, f"{row_number}-qator: kamida bitta to'g'ri javob kerak"
            continue

        qtype = _clean(row.get("question_type", "")).lower() or "single"
        if qtype not in {"single", "multiple"}:
            yield None, f"{row_number}-qator: question_type faqat single|multiple bo'ladi"
            continue
        if qtype == "single" and len(correct) > 1:
            yield None, f"{row_number}-qator: single savolda faqat bitta to'g'ri javob bo'lishi kerak"
            continue

        difficulty_raw = _clean(row.get("difficulty", ""))
        difficulty = Question.Difficulty.MEDIUM
        if difficulty_raw:
            try:
                difficulty = int(difficulty_raw)
            except ValueError:
                yield None, f"{row_number}-qator: difficulty raqam bo'lishi kerak (1|2|3)"
                continue

        status_raw = _clean(row.get("status", "")).lower() or Question.Status.PUBLISHED
        if status_raw not in dict(Question.Status.choices):
            yield None, f"{row_number}-qator: status noto'g'ri ({status_raw})"
            continue

        source_raw = _clean(row.get("source_type", "")).lower() or Question.SourceType.UNKNOWN
        if source_raw not in dict(Question.SourceType.choices):
            yield None, f"{row_number}-qator: source_type noto'g'ri ({source_raw})"
            continue

        verified_raw = _clean(row.get("is_verified", "")).lower()
        is_verified = verified_raw in {"1", "true", "yes", "on"}

        question = Question(
            subject=subject,
            topic=_resolve_topic(subject, row.get("topic", ""), create_missing),
            text_uz=text_uz,
            text_ru=_clean(row.get("text_ru", "")),
            text_en=_clean(row.get("text_en", "")),
            question_type=qtype,
            difficulty=difficulty,
            source_type=source_raw,
            status=status_raw,
            is_verified=is_verified,
            explanation_uz=_clean(row.get("explanation_uz", "")),
            explanation_ru=_clean(row.get("explanation_ru", "")),
            explanation_en=_clean(row.get("explanation_en", "")),
            created_by=created_by,
        )
        for idx, opt in enumerate(options):
            opt["sort_order"] = idx
        yield (question, options), None


def import_csv(stream, created_by=None, create_missing=False):
    """Import questions from a CSV stream. Returns ``(created, errors)``."""
    reader = csv.DictReader(stream)
    created = 0
    errors = []

    for item, err in parse_rows(reader, created_by, create_missing):
        if err:
            errors.append(err)
            continue
        question, options = item
        with transaction.atomic():
            question.save()
            QuestionOption.objects.bulk_create(
                [QuestionOption(question=question, **o) for o in options]
            )
        created += 1
    return created, errors


def export_csv(queryset, max_options=OPTION_COUNT):
    """Serialize ``queryset`` into CSV text with options as optionN columns."""
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=FIELDS)
    writer.writeheader()

    for question in queryset.prefetch_related("options").select_related("subject", "topic"):
        options = list(question.options.all())
        row = {
            "subject": question.subject.slug,
            "topic": question.topic.slug if question.topic else "",
            "text_uz": question.text_uz,
            "text_ru": question.text_ru,
            "text_en": question.text_en,
            "question_type": question.question_type,
            "difficulty": question.difficulty,
            "source_type": question.source_type,
            "status": question.status,
            "is_verified": "true" if question.is_verified else "false",
            "explanation_uz": question.explanation_uz,
            "explanation_ru": question.explanation_ru,
            "explanation_en": question.explanation_en,
        }
        for n in range(1, max_options + 1):
            opt = options[n - 1] if n - 1 < len(options) else None
            row[f"option{n}_uz"] = opt.text_uz if opt else ""
            row[f"option{n}_correct"] = "true" if (opt and opt.is_correct) else "false"
        writer.writerow(row)
    return buffer.getvalue()