from datetime import timedelta

from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Subject, Topic

from .models import PracticeAnswer, PracticeSession
from .serializers import SessionListSerializer


class StatsSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        finished = PracticeSession.objects.filter(
            user=user, status=PracticeSession.Status.FINISHED
        ).select_related("subject", "topic")

        finished_ids = list(finished.values_list("id", flat=True))

        total_questions = sum(
            finished.values_list("question_count", flat=True)
        )
        answered = sum(
            (s.correct_answers + s.incorrect_answers) for s in finished
        )
        correct = sum(s.correct_answers for s in finished)

        accuracy = round(correct / answered * 100) if answered else 0
        current_score = (
            round(sum(s.correct_answers for s in finished) / total_questions * 100)
            if total_questions
            else 0
        )

        # Subject breakdown
        by_subject = (
            finished.values("subject")
            .annotate(
                sessions=Count("id"),
                questions=Sum("question_count"),
                correct=Sum("correct_answers"),
            )
            .order_by("-sessions")
        )
        subject_ids = [row["subject"] for row in by_subject]
        names = {s.id: s for s in Subject.objects.filter(id__in=subject_ids)}
        subject_breakdown = [
            {
                "subject_id": row["subject"],
                "subject_name_uz": names[row["subject"]].name_uz,
                "subject_name_ru": names[row["subject"]].name_ru,
                "subject_name_en": names[row["subject"]].name_en,
                "slug": names[row["subject"]].slug,
                "sessions": row["sessions"],
                "questions": row["questions"],
                "correct": row["correct"],
                "accuracy": round(row["correct"] / row["questions"] * 100)
                if row["questions"]
                else 0,
            }
            for row in by_subject
        ]

        # Streak: consecutive days (ending today or yesterday) with a finished session
        dates = {
            timezone.localtime(s.finished_at).date()
            for s in finished
            if s.finished_at is not None
        }
        today = timezone.localdate()
        streak = 0
        cursor = today
        if cursor not in dates:
            cursor = today - timedelta(days=1)
        while cursor in dates:
            streak += 1
            cursor -= timedelta(days=1)

        # Weekly activity (last 7 days, including today)
        week_start = today - timedelta(days=6)
        activity = {week_start + timedelta(days=i): [0, 0] for i in range(7)}
        week_answers = (
            PracticeAnswer.objects.filter(
                session__user=user,
                session__status=PracticeSession.Status.FINISHED,
                session__finished_at__date__gte=week_start,
                selected_option__isnull=False,
            )
            .select_related("session")
        )
        for answer in week_answers:
            day = timezone.localtime(answer.answered_at).date()
            if day in activity:
                activity[day][0] += 1
                if answer.is_correct:
                    activity[day][1] += 1
        weekly_activity = [
            {
                "date": day.isoformat(),
                "answered": activity[day][0],
                "correct": activity[day][1],
            }
            for day in sorted(activity)
        ]

        # Weak topics: topics with the most wrong answers
        weak_rows = (
            PracticeAnswer.objects.filter(
                session__user=user,
                session__status=PracticeSession.Status.FINISHED,
                is_correct=False,
                question__topic__isnull=False,
            )
            .values("question__topic")
            .annotate(wrong=Count("id"))
            .order_by("-wrong")[:5]
        )
        topic_ids = [r["question__topic"] for r in weak_rows]
        topic_names = {
            t.id: t for t in Topic.objects.filter(id__in=topic_ids).select_related("subject")
        }
        weak_topics = [
            {
                "topic_id": row["question__topic"],
                "topic_name_uz": topic_names[row["question__topic"]].name_uz,
                "topic_name_ru": topic_names[row["question__topic"]].name_ru,
                "topic_name_en": topic_names[row["question__topic"]].name_en,
                "subject_name_uz": topic_names[row["question__topic"]].subject.name_uz,
                "subject_name_ru": topic_names[row["question__topic"]].subject.name_ru,
                "subject_name_en": topic_names[row["question__topic"]].subject.name_en,
                "wrong": row["wrong"],
            }
            for row in weak_rows
            if row["question__topic"] in topic_names
        ]

        recent = PracticeSession.objects.filter(
            id__in=finished_ids
        ).select_related("subject", "topic").order_by("-started_at")[:5]
        recent_sessions = SessionListSerializer(recent, many=True).data

        payload = {
            "total_finished": finished.count(),
            "total_questions": total_questions,
            "total_answered": answered,
            "accuracy": accuracy,
            "current_score": current_score,
            "streak": streak,
            "weekly_activity": weekly_activity,
            "subject_breakdown": subject_breakdown,
            "weak_topics": weak_topics,
            "recent_sessions": recent_sessions,
        }
        return Response(payload)