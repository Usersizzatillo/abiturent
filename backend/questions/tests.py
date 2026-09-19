from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Subject
from questions.models import Question, QuestionOption

User = get_user_model()


class QuestionApiTests(APITestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name_uz="Matematika", slug="matematika")
        self.teacher = User.objects.create_user(
            username="teacher1", password="Passw0rd!", role=User.Role.TEACHER
        )
        self.student = User.objects.create_user(
            username="student1", password="Passw0rd!", role=User.Role.STUDENT
        )
        self.q = Question.objects.create(
            subject=self.subject,
            text_uz="2+2 nechaga teng?",
            difficulty=Question.Difficulty.EASY,
            status=Question.Status.PUBLISHED,
            created_by=self.teacher,
        )
        QuestionOption.objects.create(question=self.q, text_uz="3", is_correct=False, sort_order=1)
        QuestionOption.objects.create(question=self.q, text_uz="4", is_correct=True, sort_order=2)
        self.draft = Question.objects.create(
            subject=self.subject,
            text_uz="Qoralama savol",
            status=Question.Status.DRAFT,
            created_by=self.teacher,
        )
        QuestionOption.objects.create(question=self.draft, text_uz="A", is_correct=True, sort_order=1)
        QuestionOption.objects.create(question=self.draft, text_uz="B", is_correct=False, sort_order=2)

    def _auth(self, user):
        self.client.force_login(user)

    def test_student_sees_only_published_without_correct(self):
        self._auth(self.student)
        res = self.client.get("/api/questions/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ids = [q["id"] for q in res.data["results"]]
        self.assertIn(self.q.id, ids)
        self.assertNotIn(self.draft.id, ids)
        first = res.data["results"][0]
        self.assertNotIn("is_correct", first["options"][0])
        self.assertNotIn("explanation_uz", first)

    def test_student_cannot_create(self):
        self._auth(self.student)
        res = self.client.post(
            "/api/questions/",
            {"subject": self.subject.id, "text_uz": "?",
             "options": [{"text_uz": "1", "is_correct": True}]},
            format="json",
        )
        self.assertIn(res.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED))

    def test_teacher_can_create_full(self):
        self._auth(self.teacher)
        res = self.client.post(
            "/api/questions/",
            {
                "subject": self.subject.id,
                "topic": None,
                "text_uz": "12*12?",
                "text_ru": "",
                "text_en": "",
                "question_type": "single",
                "difficulty": 2,
                "explanation_uz": "144",
                "source_type": "custom",
                "status": "draft",
                "options": [
                    {"text_uz": "140", "is_correct": False, "sort_order": 1},
                    {"text_uz": "144", "is_correct": True, "sort_order": 2},
                ],
            },
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        q = Question.objects.get(pk=res.data["id"])
        self.assertEqual(q.options.filter(is_correct=True).count(), 1)
        self.assertEqual(q.created_by, self.teacher)

    def test_create_requires_correct_option(self):
        self._auth(self.teacher)
        res = self.client.post(
            "/api/questions/",
            {"subject": self.subject.id, "text_uz": "?",
             "options": [{"text_uz": "1", "is_correct": False}]},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_single_requires_one_correct(self):
        self._auth(self.teacher)
        res = self.client.post(
            "/api/questions/",
            {"subject": self.subject.id, "text_uz": "?",
             "options": [
                 {"text_uz": "1", "is_correct": True},
                 {"text_uz": "2", "is_correct": True},
             ]},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_teacher_can_update_status(self):
        self._auth(self.teacher)
        res = self.client.patch(
            f"/api/questions/{self.draft.id}/", {"status": "published"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.draft.refresh_from_db()
        self.assertEqual(self.draft.status, Question.Status.PUBLISHED)

    def test_anonymous_denied(self):
        res = self.client.get("/api/questions/")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_ordering_defaults_to_newest_first(self):
        later = Question.objects.create(
            subject=self.subject,
            text_uz="Keyingi savol",
            status=Question.Status.PUBLISHED,
            created_by=self.teacher,
        )
        QuestionOption.objects.create(question=later, text_uz="A", is_correct=True, sort_order=1)
        QuestionOption.objects.create(question=later, text_uz="B", is_correct=False, sort_order=2)
        self._auth(self.student)
        res = self.client.get("/api/questions/")
        ids = [q["id"] for q in res.data["results"]]
        self.assertEqual(ids[:2], [later.id, self.q.id])

    def test_ordering_param_reversed(self):
        self._auth(self.student)
        res = self.client.get("/api/questions/", {"ordering": "id"})
        ids = [q["id"] for q in res.data["results"]]
        self.assertEqual(ids, [self.q.id])