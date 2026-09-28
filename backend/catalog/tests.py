from rest_framework import status
from rest_framework.test import APITestCase

from questions.models import Question

from .models import Subject, Subtopic, Topic


class SubjectApiTests(APITestCase):
    def setUp(self):
        self.subj = Subject.objects.create(
            name_uz="Matematika",
            name_ru="Математика",
            name_en="Mathematics",
            slug="matematika",
            code="M",
            sort_order=0,
        )
        self.hidden = Subject.objects.create(
            name_uz="Yashirin fan",
            slug="yashirin-fan",
            is_active=False,
            sort_order=99,
        )
        self.topic = Topic.objects.create(
            subject=self.subj,
            name_uz="Tenglamalar",
            slug="tenglamalar",
            sort_order=0,
        )
        Subtopic.objects.create(topic=self.topic, name_uz="Kvadrat tenglamalar")

    def test_list_subjects(self):
        res = self.client.get("/api/subjects/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["count"] >= 1)
        slugs = {s["slug"] for s in res.data["results"]}
        self.assertIn("matematika", slugs)
        self.assertNotIn("yashirin-fan", slugs)

    def test_subject_has_topic_count(self):
        res = self.client.get("/api/subjects/")
        mat = next(s for s in res.data["results"] if s["slug"] == "matematika")
        self.assertEqual(mat["topic_count"], 1)

    def test_detail_includes_topics_and_subtopics(self):
        res = self.client.get("/api/subjects/matematika/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["topics"]), 1)
        topic = res.data["topics"][0]
        self.assertEqual(topic["name_uz"], "Tenglamalar")
        self.assertEqual(len(topic["subtopics"]), 1)

    def _published_question(self, topic):
        return Question.objects.create(
            subject=self.subj,
            topic=topic,
            text_uz="x^2 = 4 ?",
            status=Question.Status.PUBLISHED,
        )

    def test_subject_detail_topic_question_count(self):
        """Nested topics must report their published question count.

        TopicSerializer reads ``_question_count`` off the instance, so a
        queryset without the annotation reports 0 for every topic.
        """
        self._published_question(self.topic)
        res = self.client.get("/api/subjects/matematika/")
        self.assertEqual(res.data["topics"][0]["question_count"], 1)

    def test_topic_question_count_ignores_drafts(self):
        Question.objects.create(
            subject=self.subj,
            topic=self.topic,
            text_uz="Draft savol",
            status=Question.Status.DRAFT,
        )
        res = self.client.get(f"/api/topics/{self.topic.id}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["question_count"], 0)

    def test_subject_topics_action_question_count(self):
        self._published_question(self.topic)
        res = self.client.get("/api/subjects/matematika/topics/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["question_count"], 1)

    def test_slug_falls_back_when_name_is_untranslatable(self):
        """Pure Cyrillic names slugify to an empty string, which used to collide
        with the next empty slug through the unique constraint."""
        first = Subject.objects.create(name_uz="Математика")
        second = Subject.objects.create(name_uz="Математика")
        self.assertTrue(first.slug)
        self.assertTrue(second.slug)
        self.assertNotEqual(first.slug, second.slug)
        sub = Subject.objects.create(name_uz="Физика")
        t1 = Topic.objects.create(subject=sub, name_uz="Кинематика")
        t2 = Topic.objects.create(subject=sub, name_uz="Кинематика")
        self.assertTrue(t1.slug)
        self.assertNotEqual(t1.slug, t2.slug)

    def test_explicit_slug_is_preserved(self):
        topic = Topic.objects.create(
            subject=self.subj, name_uz="Tenglamalar", slug="custom-slug"
        )
        self.assertEqual(topic.slug, "custom-slug")

    def test_detail_404_for_unknown(self):
        res = self.client.get("/api/subjects/nonexistent/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_can_read_anonymous(self):
        res = self.client.get("/api/subjects/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_topic_detail(self):
        res = self.client.get(f"/api/topics/{self.topic.id}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name_uz"], "Tenglamalar")

    def test_write_methods_denied(self):
        res = self.client.post("/api/subjects/", {"name_uz": "X"}, format="json")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED))