from django.contrib.auth import get_user_model
from django.db.models import Count, F, Max, Q, Sum
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from questions.models import Question, QuestionOption
from questions.serializers import QuestionFullSerializer

from .models import PracticeAnswer, PracticeSession
from .serializers import (
    LeaderboardEntrySerializer,
    PracticeAnswerInSerializer,
    PracticeAnswerResultSerializer,
    PracticeQuestionSerializer,
    PracticeStartSerializer,
    SessionListSerializer,
)

User = get_user_model()

PUBLISHED_ACTIVE = Q(is_active=True) & Q(status=Question.Status.PUBLISHED)


class LeaderboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = (
            User.objects.annotate(
                finished_sessions=Count(
                    "practice_sessions",
                    filter=Q(practice_sessions__status=PracticeSession.Status.FINISHED),
                ),
                correct_answers=Sum(
                    "practice_sessions__correct_answers",
                    filter=Q(practice_sessions__status=PracticeSession.Status.FINISHED),
                ),
                total_answered=Sum(
                    F("practice_sessions__correct_answers")
                    + F("practice_sessions__incorrect_answers"),
                    filter=Q(practice_sessions__status=PracticeSession.Status.FINISHED),
                ),
            )
            .filter(finished_sessions__gt=0, is_active=True)
            .exclude(is_staff=True, is_superuser=True)
            .order_by("-correct_answers", "-total_answered")[:10]
        )
        for rank, user in enumerate(queryset, start=1):
            user.rank = rank
        data = LeaderboardEntrySerializer(queryset, many=True).data
        return Response(data)


class PracticeSessionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]
    serializer_class = SessionListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["id", "started_at", "finished_at", "question_count", "correct_answers"]
    ordering = ["-started_at"]

    def get_queryset(self):
        return PracticeSession.objects.filter(user=self.request.user).select_related(
            "subject", "topic"
        ).prefetch_related("answers")

    def create(self, request, *args, **kwargs):
        serializer = PracticeStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        qs = Question.objects.filter(PUBLISHED_ACTIVE, subject=data["subject"])
        if data.get("topic"):
            qs = qs.filter(topic=data["topic"])
        requested = data["question_count"]
        pool = list(qs.order_by("?")[:requested])
        if not pool:
            return Response(
                {"detail": "Ushbu fan bo'yicha hozircha testlar mavjud emas."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Pool smaller than requested: shrink session to the available count so
        # tiny question banks still produce a working exam instead of a hard error.
        actual_count = len(pool)
        session = PracticeSession.objects.create(
            user=request.user,
            mode=data["mode"],
            subject=data["subject"],
            topic=data.get("topic"),
            question_count=actual_count,
        )
        session.answers.bulk_create(
            [PracticeAnswer(session=session, question=q) for q in pool]
        )
        return Response(
            self._session_payload(session, first_question=True),
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        session = self.get_object()
        return Response(self._session_payload(session))

    def _session_payload(self, session, first_question=False):
        questions = Question.objects.filter(practice_answers__session=session).order_by(
            "practice_answers__id"
        )
        payload = {
            "id": session.id,
            "mode": session.mode,
            "subject": session.subject_id,
            "topic": session.topic_id,
            "status": session.status,
            "question_count": session.question_count,
            "progress_index": session.progress_index,
            "correct_answers": session.correct_answers,
            "incorrect_answers": session.incorrect_answers,
            "started_at": session.started_at.isoformat(),
            "finished_at": session.finished_at.isoformat() if session.finished_at else None,
        }
        if first_question:
            q = questions.first()
            payload["current_question"] = (
                PracticeQuestionSerializer(q).data if q else None
            )
        return payload

    @action(detail=True, methods=["get"], url_path="current")
    def current(self, request, pk=None):
        session = self.get_object()
        if session.status == PracticeSession.Status.FINISHED:
            return Response(
                {"detail": "Sessiya yakunlangan."}, status=status.HTTP_400_BAD_REQUEST
            )
        question = (
            Question.objects.filter(practice_answers__session=session)
            .exclude(practice_answers__selected_option__isnull=False)
            .order_by("practice_answers__id")
            .first()
        )
        unanswered = session.answers.filter(selected_option__isnull=True).count()
        return Response(
            {
                "question": PracticeQuestionSerializer(question).data if question else None,
                "unanswered_count": unanswered,
            }
        )

    @action(detail=True, methods=["get"], url_path="questions", url_name="questions")
    def questions(self, request, pk=None):
        session = self.get_object()
        queryset = Question.objects.filter(practice_answers__session=session).order_by(
            "practice_answers__id"
        )
        serializer = PracticeQuestionSerializer(queryset, many=True)
        return Response({"questions": serializer.data})

    @action(detail=True, methods=["post"], url_path="answer", url_name="answer")
    def answer(self, request, pk=None):
        session = self.get_object()
        if session.status == PracticeSession.Status.FINISHED:
            return Response(
                {"detail": "Sessiya yakunlangan."}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PracticeAnswerInSerializer(
            data=request.data, context={"session": session}
        )
        serializer.is_valid(raise_exception=True)
        answer = session.answers.get(question_id=serializer.validated_data["question_id"])
        try:
            option = answer.question.options.get(pk=serializer.validated_data["option_id"])
        except QuestionOption.DoesNotExist:
            return Response(
                {"option_id": "Noto'g'ri variant."}, status=status.HTTP_400_BAD_REQUEST
            )
        is_correct = option.is_correct
        answer.selected_option = option
        answer.is_correct = is_correct
        answer.save()
        if is_correct:
            session.correct_answers = session.answers.filter(
                selected_option__isnull=False, is_correct=True
            ).count()
        else:
            session.incorrect_answers = session.answers.filter(
                selected_option__isnull=False, is_correct=False
            ).count()
        session.progress_index = session.answers.filter(
            selected_option__isnull=False
        ).count()
        session.save()
        result = PracticeAnswerResultSerializer(
            {
                "is_correct": is_correct,
                "correct_option_id": answer.question.options.filter(is_correct=True).first().id,
                "explanation_uz": answer.question.explanation_uz,
                "explanation_ru": answer.question.explanation_ru,
                "explanation_en": answer.question.explanation_en,
                "correct_count": session.correct_answers,
                "total_count": session.question_count,
            }
        )
        return Response(result.data)

    @action(detail=True, methods=["post"], url_path="finish", url_name="finish")
    def finish(self, request, pk=None):
        session = self.get_object()
        if session.status == PracticeSession.Status.FINISHED:
            return Response(
                {"detail": "Sessiya allaqachon yakunlangan."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        session.status = PracticeSession.Status.FINISHED
        session.finished_at = timezone.now()
        session.save()
        return self._finished_report(session)

    @action(detail=True, methods=["get"], url_path="report", url_name="report")
    def report(self, request, pk=None):
        session = self.get_object()
        return self._finished_report(session)

    def _finished_report(self, session):
        answers = (
            session.answers.select_related("question", "selected_option")
            .order_by("id")
            .all()
        )
        report = {
            "id": session.id,
            "mode": session.mode,
            "subject": session.subject_id,
            "status": session.status,
            "question_count": session.question_count,
            "correct_answers": session.correct_answers,
            "incorrect_answers": session.incorrect_answers,
            "unanswered": session.answers.filter(selected_option__isnull=True).count(),
            "score_percent": round(
                (session.correct_answers / session.question_count) * 100
            )
            if session.question_count
            else 0,
            "started_at": session.started_at.isoformat(),
            "finished_at": (
                session.finished_at.isoformat() if session.finished_at else None
            ),
        }
        questions = []
        for answer in answers:
            q = answer.question
            questions.append(
                {
                    "question": QuestionFullSerializer(q).data,
                    "selected_option_id": answer.selected_option_id,
                    "is_correct": answer.is_correct,
                }
            )
        report["questions"] = questions
        return Response(report)