from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Subject, Topic
from practice.models import PracticeAnswer, PracticeSession
from questions.models import Question, QuestionOption

User = get_user_model()


class PracticeApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="student1", password="Passw0rd!", role=User.Role.STUDENT
        )
        self.subject = Subject.objects.create(name_uz="Matematika", slug="matematika")
        self.q1 = Question.objects.create(
            subject=self.subject,
            text_uz="2+2?",
            explanation_uz="4 ga teng",
            status=Question.Status.PUBLISHED,
            created_by=None,
        )
        QuestionOption.objects.create(question=self.q1, text_uz="3", is_correct=False, sort_order=0)
        QuestionOption.objects.create(question=self.q1, text_uz="4", is_correct=True, sort_order=1)
        self.q2 = Question.objects.create(
            subject=self.subject,
            text_uz="3*3?",
            explanation_uz="9 ga teng",
            status=Question.Status.PUBLISHED,
        )
        QuestionOption.objects.create(question=self.q2, text_uz="9", is_correct=True, sort_order=0)
        QuestionOption.objects.create(question=self.q2, text_uz="6", is_correct=False, sort_order=1)
        self.hidden = Question.objects.create(
            subject=self.subject, text_uz="Yashirin", status=Question.Status.DRAFT
        )
        QuestionOption.objects.create(question=self.hidden, text_uz="A", is_correct=True, sort_order=0)
        self.client.force_login(self.user)

    def _start(self, count=2):
        return self.client.post(
            "/api/sessions/",
            {"subject": self.subject.id, "question_count": count, "mode": "practice"},
            format="json",
        )

    def test_start_session_returns_current_question(self):
        res = self._start()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("current_question", res.data)
        self.assertNotIn("is_correct", res.data["current_question"]["options"][0])

    def test_start_empty_pool_rejected(self):
        empty = Subject.objects.create(name_uz="Bo'sh fan", slug="bosh-fan")
        res = self.client.post(
            "/api/sessions/",
            {"subject": empty.id, "question_count": 10, "mode": "practice"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_correct(self):
        session = self._start().data
        option_id = self.q1.options.get(is_correct=True).id
        res = self.client.post(
            f"/api/sessions/{session['id']}/answer/",
            {"question_id": self.q1.id, "option_id": option_id},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["is_correct"])
        self.assertEqual(res.data["correct_option_id"], self.q1.options.get(is_correct=True).id)
        self.assertEqual(res.data["correct_count"], 1)

    def test_answer_wrong_records_incorrect(self):
        session = self._start().data
        option_id = self.q1.options.get(is_correct=False).id
        res = self.client.post(
            f"/api/sessions/{session['id']}/answer/",
            {"question_id": self.q1.id, "option_id": option_id},
            format="json",
        )
        self.assertFalse(res.data["is_correct"])
        self.assertEqual(res.data["correct_count"], 0)

    def test_cannot_answer_same_question_twice(self):
        session = self._start().data
        option_id = self.q1.options.get(is_correct=True).id
        self.client.post(
            f"/api/sessions/{session['id']}/answer/",
            {"question_id": self.q1.id, "option_id": option_id},
            format="json",
        )
        res = self.client.post(
            f"/api/sessions/{session['id']}/answer/",
            {"question_id": self.q1.id, "option_id": option_id},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_finish_reports_score(self):
        session = self._start().data
        correct_id = self.q1.options.get(is_correct=True).id
        wrong_id = self.q2.options.get(is_correct=False).id
        self.client.post(
            f"/api/sessions/{session['id']}/answer/",
            {"question_id": self.q1.id, "option_id": correct_id},
            format="json",
        )
        self.client.post(
            f"/api/sessions/{session['id']}/answer/",
            {"question_id": self.q2.id, "option_id": wrong_id},
            format="json",
        )
        res = self.client.post(f"/api/sessions/{session['id']}/finish/", format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["correct_answers"], 1)
        self.assertEqual(res.data["incorrect_answers"], 1)
        self.assertEqual(res.data["score_percent"], 50)
        self.assertEqual(len(res.data["questions"]), 2)
        self.assertIn("is_correct", res.data["questions"][0]["question"]["options"][0])

    def test_current_after_some_answers(self):
        session = self._start().data
        option_id = self.q1.options.get(is_correct=True).id
        self.client.post(
            f"/api/sessions/{session['id']}/answer/",
            {"question_id": self.q1.id, "option_id": option_id},
            format="json",
        )
        res = self.client.get(f"/api/sessions/{session['id']}/current/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["question"]["id"], self.q2.id)
        self.assertEqual(res.data["unanswered_count"], 1)

    def test_other_user_cannot_access(self):
        other = User.objects.create_user(
            username="student2", password="Passw0rd!", role=User.Role.STUDENT
        )
        self.client.force_login(other)
        res = self.client.get(f"/api/sessions/99999/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_sessions_returns_summaries(self):
        self._start()
        res = self.client.get("/api/sessions/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)
        row = res.data["results"][0]
        self.assertEqual(row["mode"], "practice")
        self.assertEqual(row["subject"]["name_uz"], "Matematika")
        self.assertEqual(row["score_percent"], 0)
        self.assertEqual(row["unanswered"], 2)

    def test_stats_summary_aggregates(self):
        session = self._start().data
        correct_id = self.q1.options.get(is_correct=True).id
        wrong_id = self.q2.options.get(is_correct=False).id
        self.client.post(
            f"/api/sessions/{session['id']}/answer/",
            {"question_id": self.q1.id, "option_id": correct_id},
            format="json",
        )
        self.client.post(
            f"/api/sessions/{session['id']}/answer/",
            {"question_id": self.q2.id, "option_id": wrong_id},
            format="json",
        )
        self.client.post(f"/api/sessions/{session['id']}/finish/", format="json")

        res = self.client.get("/api/stats/summary/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["total_finished"], 1)
        self.assertEqual(res.data["total_answered"], 2)
        self.assertEqual(res.data["accuracy"], 50)
        self.assertEqual(res.data["current_score"], 50)
        self.assertEqual(res.data["streak"], 1)
        self.assertEqual(len(res.data["weekly_activity"]), 7)
        self.assertEqual(res.data["weekly_activity"][-1]["answered"], 2)
        self.assertEqual(res.data["recent_sessions"][0]["score_percent"], 50)

        subj = next(
            s for s in res.data["subject_breakdown"] if s["subject_id"] == self.subject.id
        )
        self.assertEqual(subj["accuracy"], 50)
        self.assertEqual(subj["sessions"], 1)

        with self.subTest("weak_topics"):
            topic = Topic.objects.create(
                subject=self.subject, name_uz="Hisob-kitob", slug="hisob-kitob"
            )
            self.q2.topic = topic
            self.q2.save(update_fields=["topic"])
            cm = self.client
            res2 = self.client.get("/api/stats/summary/")
            self.assertGreaterEqual(len(res2.data["weak_topics"]), 1)

    def test_questions_list_hides_correct_answers(self):
        session = self._start().data
        res = self.client.get(f"/api/sessions/{session['id']}/questions/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["questions"]), 2)
        for q in res.data["questions"]:
            for option in q["options"]:
                self.assertNotIn("is_correct", option)

    def test_report_readonly_after_answer(self):
        session = self._start().data
        correct_id = self.q1.options.get(is_correct=True).id
        self.client.post(
            f"/api/sessions/{session['id']}/answer/",
            {"question_id": self.q1.id, "option_id": correct_id},
            format="json",
        )
        res = self.client.get(f"/api/sessions/{session['id']}/report/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["status"], "in_progress")
        self.assertEqual(res.data["correct_answers"], 1)
        self.assertEqual(len(res.data["questions"]), 2)
        answered = next(
            q for q in res.data["questions"] if q["question"]["id"] == self.q1.id
        )
        self.assertEqual(answered["is_correct"], True)
        self.assertEqual(answered["selected_option_id"], correct_id)
        self.assertIn("explanation_uz", answered["question"])

    def test_stats_requires_auth(self):
        fresh = self.client.__class__()
        self.assertEqual(
            fresh.get("/api/stats/summary/").status_code,
            status.HTTP_403_FORBIDDEN,
        )