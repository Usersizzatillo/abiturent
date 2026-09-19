from django.conf import settings
from django.db import models

from catalog.models import Subject, Topic
from questions.models import Question, QuestionOption


class PracticeSession(models.Model):
    class Mode(models.TextChoices):
        PRACTICE = "practice", "Mashq"
        EXAM = "exam", "Sinov imtihoni"

    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "Jarayonda"
        FINISHED = "finished", "Yakunlangan"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="practice_sessions",
        on_delete=models.CASCADE,
    )
    mode = models.CharField(
        max_length=20, choices=Mode.choices, default=Mode.PRACTICE, db_index=True
    )
    subject = models.ForeignKey(
        Subject, related_name="practice_sessions", on_delete=models.PROTECT
    )
    topic = models.ForeignKey(
        Topic, related_name="practice_sessions", on_delete=models.PROTECT, null=True, blank=True
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.IN_PROGRESS, db_index=True
    )
    question_count = models.PositiveIntegerField(default=10)
    progress_index = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]
        db_table = "practice_session"

    def __str__(self):
        return f"{self.user} - {self.subject} ({self.mode})"


class PracticeAnswer(models.Model):
    session = models.ForeignKey(
        PracticeSession, related_name="answers", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question, related_name="practice_answers", on_delete=models.PROTECT
    )
    selected_option = models.ForeignKey(
        QuestionOption,
        related_name="selections",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        db_table = "practice_answer"
        constraints = [
            models.UniqueConstraint(
                fields=["session", "question"], name="uniq_session_question"
            )
        ]

    def __str__(self):
        return f"{self.session_id} -> {self.question_id}"