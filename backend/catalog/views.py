from django.db.models import Count, Prefetch, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Subject, Topic
from .serializers import SubjectDetailSerializer, SubjectSerializer, TopicSerializer

PUBLISHED = Q(questions__is_active=True) & Q(questions__status="published")


def _annotated_topics():
    """Active topics with their published question count already resolved.

    TopicSerializer reads ``_question_count`` off the instance, so any queryset
    that is *not* annotated silently reports 0 questions per topic.
    """
    return (
        Topic.active.all()
        .annotate(_question_count=Count("questions", filter=PUBLISHED, distinct=True))
        .prefetch_related("subtopics")
        .order_by("sort_order", "id")
    )


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
            .prefetch_related(Prefetch("topics", queryset=_annotated_topics()))
        )

    @action(detail=True, methods=["get"], url_path="topics")
    def topics(self, request, slug=None):
        # lookup_field is "slug", so the detail route passes the slug as the
        # keyword argument name, not "pk".
        subject = self.get_object()
        return Response(
            TopicSerializer(
                _annotated_topics().filter(subject=subject),
                many=True,
                context={"request": request},
            ).data
        )


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.active.all()
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return _annotated_topics()