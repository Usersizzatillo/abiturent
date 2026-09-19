from rest_framework import serializers

from .models import Subject, Subtopic, Topic


class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic
        fields = ["id", "name_uz", "name_ru", "name_en", "sort_order"]


class TopicSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    subtopics = SubtopicSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "name_en",
            "slug",
            "sort_order",
            "question_count",
            "subtopics",
        ]

    def get_question_count(self, obj):
        return getattr(obj, "_question_count", 0)


class SubjectBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name_uz", "name_ru", "name_en", "slug"]


class SubjectSerializer(serializers.ModelSerializer):
    topic_count = serializers.SerializerMethodField()
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "name_en",
            "slug",
            "code",
            "icon",
            "sort_order",
            "topic_count",
            "question_count",
        ]

    def get_topic_count(self, obj):
        return getattr(obj, "_topic_count", 0)

    def get_question_count(self, obj):
        return getattr(obj, "_question_count", 0)


class SubjectDetailSerializer(SubjectSerializer):
    topics = TopicSerializer(many=True, read_only=True)

    class Meta(SubjectSerializer.Meta):
        fields = SubjectSerializer.Meta.fields + ["topics"]