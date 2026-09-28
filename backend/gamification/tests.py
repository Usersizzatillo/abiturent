from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Subject
from gamification.models import Badge
from gamification.services import sync_badges, user_stats
from practice.models import PracticeAnswer, PracticeSession
from questions.models import Question, QuestionOption

User = get_user_model()


class GamificationApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="student1", password="Passw0rd!", role=User.Role.STUDENT
        )
        self.subject = Subject.objects.create(name_uz="Matematika", slug="matematika")
        self.q = Question.objects.create(
            subject=self.subject, text_uz="2+2?", status=Question.Status.PUBLISHED
        )
        QuestionOption.objects.create(question=self.q, text_uz="4", is_correct=True, sort_order=0)
        QuestionOption.objects.create(question=self.q, text_uz="3", is_correct=False, sort_order=1)
        call_command("seed_badges")
        self.client.force_login(self.user)

    def _finish_correct_session(self):
        start = self.client.post(
            "/api/sessions/",
            {"subject": self.subject.id, "question_count": 1, "mode": "practice"},
            format="json",
        )
        session_id = start.data["id"]
        option_id = self.q.options.get(is_correct=True).id
        self.client.post(
            f"/api/sessions/{session_id}/answer/",
            {"question_id": self.q.id, "option_id": option_id},
            format="json",
        )
        return self.client.post(f"/api/sessions/{session_id}/finish/", {}, format="json")

    def test_seed_badges_present(self):
        self.assertEqual(Badge.objects.count(), 12)

    def test_badges_listed_unearned(self):
        res = self.client.get("/api/gamification/badges/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["badges"]), 12)
        self.assertEqual(res.data["earned_count"], 0)
        self.assertFalse(res.data["badges"][0]["earned"])

    def test_finish_unlocks_first_badge(self):
        res = self._finish_correct_session()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        codes = [b["code"] for b in res.data["new_badges"]]
        self.assertIn("first-steps", codes)
        self.assertIn("perfect-100", codes)

        res = self.client.get("/api/gamification/badges/")
        first = [b for b in res.data["badges"] if b["code"] == "first-steps"][0]
        self.assertTrue(first["earned"])

    def test_sync_badges_is_idempotent(self):
        session = PracticeSession.objects.create(
            user=self.user,
            mode=PracticeSession.Mode.PRACTICE,
            subject=self.subject,
            status=PracticeSession.Status.FINISHED,
            question_count=1,
            correct_answers=1,
            finished_at=None,
        )
        PracticeAnswer.objects.create(
            session=session, question=self.q, is_correct=True
        )
        new = sync_badges(self.user)
        self.assertIn("first-steps", [b.code for b in new])
        again = sync_badges(self.user)
        self.assertEqual([b.code for b in again], [])

    def test_stats_xp_and_level(self):
        self._finish_correct_session()
        res = self.client.get("/api/stats/summary/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["level"]["xp"], 10)
        self.assertEqual(res.data["level"]["level"], 1)

    def test_user_stats_streak_and_sessions(self):
        stats = user_stats(self.user)
        self.assertEqual(stats["finished_sessions"], 0)
        self.assertEqual(stats["streak"], 0)