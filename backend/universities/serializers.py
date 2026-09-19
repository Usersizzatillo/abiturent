from rest_framework import serializers

from catalog.serializers import SubjectBriefSerializer

from .models import Direction, University


class DirectionSerializer(serializers.ModelSerializer):
    subjects = SubjectBriefSerializer(many=True, read_only=True)
    university = serializers.SerializerMethodField()

    class Meta:
        model = Direction
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "name_en",
            "code",
            "university",
            "subjects",
            "duration_years",
            "quota",
            "grant_places",
            "paid_places",
            "is_active",
        ]

    def get_university(self, obj):
        return {
            "slug": obj.university.slug,
            "name_uz": obj.university.name_uz,
            "name_ru": obj.university.name_ru,
            "name_en": obj.university.name_en,
        }


class UniversitySerializer(serializers.ModelSerializer):
    direction_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = University
        fields = [
            "id",
            "slug",
            "name_uz",
            "name_ru",
            "name_en",
            "code",
            "city_uz",
            "city_ru",
            "city_en",
            "established",
            "website",
            "description_uz",
            "description_ru",
            "description_en",
            "direction_count",
        ]


class UniversityDetailSerializer(UniversitySerializer):
    directions = DirectionSerializer(many=True, read_only=True)

    class Meta(UniversitySerializer.Meta):
        fields = UniversitySerializer.Meta.fields + ["directions"]