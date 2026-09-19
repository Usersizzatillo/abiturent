from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from .models import Question
from .permissions import CanManageQuestions
from .serializers import QuestionBrowseSerializer, QuestionFullSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related("subject", "topic", "subtopic")
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["subject", "topic", "subtopic", "difficulty", "status"]
    ordering_fields = ["id", "difficulty", "created_at", "updated_at"]
    ordering = ["-created_at"]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        perms = [IsAuthenticated()]
        if self.action in ("create", "update", "partial_update", "destroy"):
            perms.append(CanManageQuestions())
        return perms

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff or user.role in ("teacher", "admin"):
            return QuestionFullSerializer
        return QuestionBrowseSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff or user.role in ("teacher", "admin"):
            return qs.prefetch_related("options")
        return qs.filter(
            Q(is_active=True), Q(status=Question.Status.PUBLISHED)
        ).prefetch_related("options")