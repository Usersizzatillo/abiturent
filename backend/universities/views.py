from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Direction, University
from .serializers import (
    DirectionSerializer,
    UniversityDetailSerializer,
    UniversitySerializer,
)


class UniversityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = University.active.all()
    lookup_field = "slug"
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UniversityDetailSerializer
        return UniversitySerializer

    def get_queryset(self):
        return (
            University.active.all()
            .prefetch_related("directions__subjects")
            .annotate(
                direction_count=Count(
                    "directions", filter=Q(directions__is_active=True), distinct=True
                )
            )
            .order_by("sort_order", "id")
        )

    def retrieve(self, request, slug=None):
        university = self.get_object()
        serializer = UniversityDetailSerializer(
            university,
            context={"request": request},
        )
        return Response(serializer.data)


class DirectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Direction.active.all()
    serializer_class = DirectionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Direction.active.all().select_related("university").prefetch_related("subjects")
        university = self.request.query_params.get("university")
        if university:
            qs = qs.filter(university__slug=university)
        subject = self.request.query_params.get("subject")
        if subject:
            qs = qs.filter(subjects__id=subject)
        return qs.order_by("id")