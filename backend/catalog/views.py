from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Subject, Topic
from .serializers import SubjectDetailSerializer, SubjectSerializer, TopicSerializer

PUBLISHED = Q(questions__is_active=True) & Q(questions__status="published")


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.active.all()
    lookup_field = "slug"
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SubjectDetailSerializer
        return SubjectSerializer

    def get_queryset(self):
        return (
            Subject.active.all()
            .annotate(
                _topic_count=Count("topics", distinct=True),
                _question_count=Count("questions", filter=PUBLISHED, distinct=True),
            )
            .order_by("sort_order", "id")
            .prefetch_related("topics__subtopics")
        )

    @action(detail=True, methods=["get"], url_path="topics")
    def topics(self, request, pk=None):
        subject = self.get_object()
        topics = (
            Topic.active.filter(subject=subject)
            .prefetch_related("subtopics")
            .annotate(
                _question_count=Count("questions", filter=PUBLISHED, distinct=True)
            )
            .order_by("sort_order", "id")
        )
        serializer = TopicSerializer(
            topics, many=True, context={"request": request}
        )
        return Response(serializer.data)


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.active.all()
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]