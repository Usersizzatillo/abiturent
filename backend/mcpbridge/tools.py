"""
MCP tool'implementatsiyasi.

Har bir tool foydalanuvchiga (o'qituvchi / AI agent) platformadagi
universitet, yo'nalish, fan, mavzu va test savollari ma'lumotlariga
xavfsiz (javob yashirilgan) kirish imkonini beradi.

include_answers=True faqat o'qituvchi/admin foydalanishi uchun javob
variantini ochadi. Boshqa holatda to'g'ri javob hech qachon chiqmaydi.
"""

from __future__ import annotations

from typing import Optional


def _subtopic_dict(st) -> dict:
    return {
        "id": st.id,
        "name_uz": st.name_uz or st.name_ru,
        "name_ru": st.name_ru,
        "name_en": st.name_en,
    }


def _topic_dict(t) -> dict:
    return {
        "id": t.id,
        "slug": t.slug,
        "name_uz": t.name_uz or t.name_ru,
        "name_ru": t.name_ru,
        "name_en": t.name_en,
        "subtopics": [
            _subtopic_dict(s)
            for s in t.subtopics.filter(is_active=True).order_by("sort_order", "id")
        ],
    }


def _subject_dict(s, include_topics: bool = False) -> dict:
    data = {
        "id": s.id,
        "slug": s.slug,
        "code": s.code,
        "icon": s.icon,
        "name_uz": s.name_uz or s.name_ru,
        "name_ru": s.name_ru,
        "name_en": s.name_en,
    }
    if include_topics:
        data["topics"] = [
            _topic_dict(t)
            for t in s.topics.filter(is_active=True).order_by("sort_order", "id")
        ]
    return data


def _direction_dict(d) -> dict:
    subjects = [_subject_dict(s) for s in d.subjects.filter(is_active=True)]
    return {
        "id": d.id,
        "code": d.code,
        "name_uz": d.name_uz or d.name_ru,
        "name_ru": d.name_ru,
        "name_en": d.name_en,
        "duration_years": d.duration_years,
        "quota": d.quota,
        "grant_places": d.grant_places,
        "paid_places": d.paid_places,
        "subjects": subjects,
    }


def _university_dict(u, include_directions: bool = False) -> dict:
    data = {
        "id": u.id,
        "slug": u.slug,
        "code": u.code,
        "name_uz": u.name_uz or u.name_ru,
        "name_ru": u.name_ru,
        "name_en": u.name_en,
        "city_uz": u.city_uz or u.city_ru,
        "city_ru": u.city_ru,
        "city_en": u.city_en,
        "established": u.established,
        "website": u.website,
        "description_uz": u.description_uz or u.description_ru,
        "description_ru": u.description_ru,
        "description_en": u.description_en,
    }
    if include_directions:
        data["directions"] = [
            _direction_dict(d)
            for d in u.directions.filter(is_active=True).order_by("sort_order", "id")
        ]
    return data


def _question_dict(q, include_answers: bool = False) -> dict:
    options = []
    for o in q.options.all():
        item = {
            "id": o.id,
            "text": o.text_uz or o.text_ru or o.text_en,
            "text_uz": o.text_uz,
            "text_ru": o.text_ru,
            "text_en": o.text_en,
        }
        if include_answers:
            item["is_correct"] = o.is_correct
        options.append(item)

    data = {
        "id": q.id,
        "text": q.text_uz or q.text_ru or q.text_en,
        "text_uz": q.text_uz,
        "text_ru": q.text_ru,
        "text_en": q.text_en,
        "subject": _subject_dict(q.subject),
        "question_type": q.question_type,
        "difficulty": q.difficulty,
        "source_type": q.source_type,
        "is_official": q.is_official,
        "is_verified": q.is_verified,
        "options": options,
    }
    if q.topic_id:
        data["topic"] = {"id": q.topic.id, "slug": q.topic.slug, "name": q.topic.name_uz}
    if q.subtopic_id:
        data["subtopic"] = {"id": q.subtopic.id, "name": q.subtopic.name_uz}
    if include_answers:
        data["correct_indexes"] = [
            idx for idx, o in enumerate(q.options.all()) if o.is_correct
        ]
        data["explanation"] = q.explanation_uz or q.explanation_ru
    return data


def search_subjects(include_topics: bool = False) -> list[dict]:
    from catalog.models import Subject

    return [
        _subject_dict(s, include_topics=include_topics)
        for s in Subject.active.order_by("sort_order", "id")
    ]


def get_subject(slug: str, include_topics: bool = True) -> Optional[dict]:
    from catalog.models import Subject

    try:
        subject = Subject.active.get(slug=slug)
    except Subject.DoesNotExist:
        return None
    return _subject_dict(subject, include_topics=include_topics)


def search_universities(city: Optional[str] = None, limit: int = 50) -> list[dict]:
    from universities.models import University

    qs = University.active.order_by("sort_order", "id")
    if city:
        qs = qs.filter(city_uz__icontains=city) | qs.filter(city_ru__icontains=city)
    limit = max(1, min(int(limit), 200))
    return [_university_dict(u) for u in qs[:limit]]


def get_university(slug: str, include_directions: bool = True) -> Optional[dict]:
    from universities.models import University

    try:
        university = University.active.get(slug=slug)
    except University.DoesNotExist:
        return None
    return _university_dict(university, include_directions=include_directions)


def search_directions(
    subject_slug: Optional[str] = None,
    university_slug: Optional[str] = None,
    limit: int = 100,
) -> list[dict]:
    from universities.models import Direction, University

    qs = Direction.active.order_by("sort_order", "id").select_related("university")
    if subject_slug:
        qs = qs.filter(subjects__slug=subject_slug)
    if university_slug:
        try:
            university = University.active.get(slug=university_slug)
            qs = qs.filter(university=university)
        except University.DoesNotExist:
            return []
    limit = max(1, min(int(limit), 200))
    result = []
    for d in qs[:limit]:
        item = {
            "id": d.id,
            "code": d.code,
            "name_uz": d.name_uz or d.name_ru,
            "name_ru": d.name_ru,
            "name_en": d.name_en,
            "duration_years": d.duration_years,
            "quota": d.quota,
            "grant_places": d.grant_places,
            "paid_places": d.paid_places,
            "university": _university_dict(d.university),
            "subjects": [_subject_dict(s) for s in d.subjects.filter(is_active=True)],
        }
        result.append(item)
    return result


def search_questions(
    subject_slug: Optional[str] = None,
    topic_slug: Optional[str] = None,
    difficulty: Optional[int] = None,
    include_answers: bool = False,
    limit: int = 20,
) -> list[dict]:
    from questions.models import Question

    qs = Question.objects.filter(is_active=True, status=Question.Status.PUBLISHED)
    if subject_slug:
        qs = qs.filter(subject__slug=subject_slug)
    if topic_slug:
        qs = qs.filter(topic__slug=topic_slug)
    if difficulty is not None:
        qs = qs.filter(difficulty=int(difficulty))
    limit = max(1, min(int(limit), 100))
    return [
        _question_dict(q, include_answers=include_answers)
        for q in qs.select_related("subject", "topic", "subtopic")[:limit]
    ]


def get_question(question_id: int, include_answers: bool = False) -> Optional[dict]:
    from questions.models import Question

    try:
        q = Question.objects.select_related("subject", "topic", "subtopic").get(
            id=int(question_id)
        )
    except (Question.DoesNotExist, TypeError, ValueError):
        return None
    return _question_dict(q, include_answers=include_answers)


def platform_summary() -> dict:
    from catalog.models import Subject
    from questions.models import Question
    from universities.models import Direction, University

    return {
        "subjects": Subject.active.count(),
        "universities": University.active.count(),
        "directions": Direction.active.count(),
        "published_questions": Question.objects.filter(
            is_active=True, status=Question.Status.PUBLISHED
        ).count(),
    }