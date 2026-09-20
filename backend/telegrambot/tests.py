from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from catalog.models import Subject
from questions.models import Question

from . import services

User = get_user_model()


class TelegramServicesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="student1",
            password="Passw0rd!",
            role=User.Role.STUDENT,
        )
        self.subject = Subject.objects.create(name_uz="Matematika", slug="matematika")
        self.question = Question.objects.create(
            subject=self.subject,
            text_uz="2+2 nechaga teng?",
            explanation_uz="4 ga teng",
            status=Question.Status.DRAFT,
            created_by=None,
        )

    def test_new_user_text_contains_username(self):
        text = services.new_user_text(self.user)
        self.assertIn("student1", text)
        self.assertIn("Abituriyent", text)

    def test_question_submitted_text_contains_subject(self):
        author = User.objects.create_user(
            username="teach1", password="Passw0rd!", role=User.Role.TEACHER
        )
        self.question.created_by = author
        self.question.save()
        text = services.question_submitted_text(self.question)
        self.assertIn("Matematika", text)
        self.assertIn("teach1", text)
        self.assertIn("2+2", text)

    def test_daily_stats_text_contains_today(self):
        text = services.daily_stats_text()
        self.assertIn(timezone.localdate().strftime("%d.%m.%Y"), text)
        self.assertIn("Abiturend", text)

    def test_send_message_noop_when_unconfigured(self):
        results = services.send_message("hello")
        self.assertEqual(results, [])

    def test_is_configured_false_by_default(self):
        with self.settings(TELEGRAM_BOT_TOKEN="", TELEGRAM_CHAT_ID=""):
            self.assertFalse(services.is_configured())