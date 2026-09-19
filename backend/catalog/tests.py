from rest_framework import status
from rest_framework.test import APITestCase

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