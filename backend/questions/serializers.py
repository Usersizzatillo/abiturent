from django.db import transaction
from rest_framework import serializers

from .models import Question, QuestionOption


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ["id", "text_uz", "text_ru", "text_en", "is_correct", "sort_order"]


def _option_dicts(instances):
    return [
        {
            "id": o.id,
            "text_uz": o.text_uz,
            "text_ru": o.text_ru,
            "text_en": o.text_en,
            "is_correct": o.is_correct,
            "sort_order": o.sort_order,
        }
        for o in instances
    ]


def _renumber(options):
    for idx, opt in enumerate(options):
        opt["sort_order"] = idx
    return options


class QuestionFullSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "subject",
            "topic",
            "subtopic",
            "text_uz",
            "text_ru",
            "text_en",
            "question_type",
            "difficulty",
            "explanation_uz",
            "explanation_ru",
            "explanation_en",
            "source_type",
            "is_official",
            "is_verified",
            "status",
            "created_by",
            "options",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by"]

    def validate(self, attrs):
        options = attrs.get("options")
        if options is None:
            if self.instance is None:
                raise serializers.ValidationError({"options": "Variantlar majburiy."})
            options = _option_dicts(self.instance.options.all())
        options = _renumber(options)
        attrs["options"] = options
        correct = [o for o in options if o.get("is_correct")]
        if not correct:
            raise serializers.ValidationError(
                {"options": "Kamida bitta to'g'ri javob bo'lishi kerak."}
            )
        qtype = attrs.get("question_type") or (
            self.instance.question_type if self.instance else "single"
        )
        if qtype == "single" and len(correct) > 1:
            raise serializers.ValidationError(
                {"options": "Bitta to'g'ri javobli savolda faqat bitta variant to'g'ri bo'lishi kerak."}
            )
        if len(options) < 2:
            raise serializers.ValidationError({"options": "Kamida 2 ta variant kerak."})
        return attrs

    def create(self, validated_data):
        options = validated_data.pop("options", [])
        validated_data["created_by"] = self.context["request"].user
        with transaction.atomic():
            question = Question.objects.create(**validated_data)
            self._sync_options(question, options)
        return question

    def update(self, instance, validated_data):
        options = validated_data.pop("options", None)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            if options is not None:
                self._sync_options(instance, options)
        return instance

    def _sync_options(self, question, options):
        kept = []
        for opt in options:
            opt_id = opt.get("id")
            obj = None
            if opt_id:
                obj = question.options.filter(pk=opt_id).first()
            if obj is None:
                obj = QuestionOption(question=question)
            for key, value in opt.items():
                if key != "id":
                    setattr(obj, key, value)
            obj.save()
            kept.append(obj.id)
        question.options.exclude(pk__in=kept).delete()


class QuestionOptionBrowse(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ["id", "text_uz", "text_ru", "text_en", "sort_order"]


class QuestionBrowseSerializer(serializers.ModelSerializer):
    options = QuestionOptionBrowse(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "subject",
            "topic",
            "subtopic",
            "text_uz",
            "text_ru",
            "text_en",
            "question_type",
            "difficulty",
            "options",
        ]