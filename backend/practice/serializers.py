from django.db.models import Q
from rest_framework import serializers

from catalog.serializers import SubjectBriefSerializer
from questions.models import Question, QuestionOption
from questions.serializers import QuestionOptionBrowse

from .models import PracticeAnswer, PracticeSession

PUBLISHED_ACTIVE = Q(is_active=True) & Q(status=Question.Status.PUBLISHED)


class PracticeStartSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(min_value=1, max_value=30, default=10)

    class Meta:
        model = PracticeSession
        fields = ["id", "mode", "subject", "topic", "question_count"]
        read_only_fields = ["id"]


class SessionListSerializer(serializers.ModelSerializer):
    subject = SubjectBriefSerializer(read_only=True)
    topic_name_uz = serializers.CharField(source="topic.name_uz", default=None)
    topic_name_ru = serializers.CharField(source="topic.name_ru", default=None)
    topic_name_en = serializers.CharField(source="topic.name_en", default=None)
    unanswered = serializers.SerializerMethodField()
    score_percent = serializers.SerializerMethodField()

    class Meta:
        model = PracticeSession
        fields = [
            "id",
            "mode",
            "subject",
            "topic",
            "topic_name_uz",
            "topic_name_ru",
            "topic_name_en",
            "status",
            "question_count",
            "progress_index",
            "correct_answers",
            "incorrect_answers",
            "unanswered",
            "score_percent",
            "started_at",
            "finished_at",
        ]

    def get_unanswered(self, obj) -> int:
        return obj.question_count - obj.progress_index

    def get_score_percent(self, obj) -> int:
        if not obj.question_count:
            return 0
        return round((obj.correct_answers / obj.question_count) * 100)


class OptionWithAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ["id", "text_uz", "text_ru", "text_en", "is_correct", "sort_order"]


class PracticeQuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionBrowse(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "text_uz",
            "text_ru",
            "text_en",
            "question_type",
            "difficulty",
            "options",
        ]


class PracticeAnswerInSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(min_value=1)
    option_id = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        session = self.context["session"]
        practice_answer = session.answers.filter(
            question_id=attrs["question_id"], selected_option__isnull=False
        ).first()
        if practice_answer is not None:
            raise serializers.ValidationError(
                {"question_id": "Bu savolga allaqachon javob berilgan."}
            )
        return attrs


class PracticeAnswerResultSerializer(serializers.Serializer):
    is_correct = serializers.BooleanField()
    correct_option_id = serializers.IntegerField()
    explanation_uz = serializers.CharField()
    explanation_ru = serializers.CharField()
    explanation_en = serializers.CharField()
    correct_count = serializers.IntegerField()
    total_count = serializers.IntegerField()