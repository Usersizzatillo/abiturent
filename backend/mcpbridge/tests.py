from django.test import TestCase

from catalog.models import Subject, Subtopic, Topic
from questions.models import Question, QuestionOption
from universities.models import Direction, University

from . import tools


class McpToolsTests(TestCase):
    def setUp(self):
        self.math = Subject.objects.create(name_uz="Matematika", slug="matematika", sort_order=0)
        self.ona = Subject.objects.create(name_uz="Ona tili", slug="ona-tili", sort_order=1)
        self.topic = Topic.objects.create(name_uz="Algebra", slug="algebra", subject=self.math)
        self.sub = Subtopic.objects.create(name_uz="Funksiyalar", topic=self.topic)

        self.uni = University.objects.create(
            name_uz="O'zbekiston Milliy universiteti",
            slug="numu",
            city_uz="Toshkent",
            sort_order=0,
        )
        self.dir = Direction.objects.create(
            university=self.uni,
            name_uz="Amaliy matematika",
            code="am",
            duration_years=4,
            sort_order=0,
        )
        self.dir.subjects.add(self.math)

        self.q = Question.objects.create(
            subject=self.math,
            topic=self.topic,
            subtopic=self.sub,
            text_uz="2+2 nechaga teng?",
            difficulty=Question.Difficulty.EASY,
            status=Question.Status.PUBLISHED,
            is_active=True,
            explanation_uz="2+2=4",
        )
        self.opt1 = QuestionOption.objects.create(
            question=self.q, text_uz="3", is_correct=False, sort_order=0
        )
        self.opt2 = QuestionOption.objects.create(
            question=self.q, text_uz="4", is_correct=True, sort_order=1
        )

    def test_platform_summary(self):
        data = tools.platform_summary()
        self.assertEqual(data["subjects"], 2)
        self.assertEqual(data["universities"], 1)
        self.assertEqual(data["directions"], 1)
        self.assertEqual(data["published_questions"], 1)

    def test_search_subjects_includes_topics(self):
        subjects = tools.search_subjects(include_topics=True)
        math = next(s for s in subjects if s["slug"] == "matematika")
        self.assertEqual(math["topics"][0]["name_uz"], "Algebra")
        self.assertEqual(math["topics"][0]["subtopics"][0]["name_uz"], "Funksiyalar")

    def test_get_subject_unknown_returns_none(self):
        self.assertIsNone(tools.get_subject("yoq"))

    def test_search_universities_city_filter(self):
        res = tools.search_universities(city="Toshkent")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["slug"], "numu")

    def test_get_university_includes_directions(self):
        uni = tools.get_university("numu")
        self.assertEqual(len(uni["directions"]), 1)
        self.assertEqual(uni["directions"][0]["subjects"][0]["slug"], "matematika")

    def test_search_directions_by_subject(self):
        res = tools.search_directions(subject_slug="matematika")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["university"]["slug"], "numu")

    def test_search_directions_by_university(self):
        res = tools.search_directions(university_slug="numu")
        self.assertEqual(len(res), 1)
        res2 = tools.search_directions(university_slug="noma'lum")
        self.assertEqual(res2, [])

    def test_search_questions_hides_answers_by_default(self):
        res = tools.search_questions(limit=10)
        item = next(q for q in res if q["id"] == self.q.id)
        self.assertNotIn("is_correct", item["options"][0])
        self.assertNotIn("correct_indexes", item)
        self.assertNotIn("explanation", item)
        self.assertEqual(item["topic"]["slug"], "algebra")

    def test_search_questions_with_answers(self):
        res = tools.search_questions(
            subject_slug="matematika", difficulty=1, include_answers=True
        )
        item = res[0]
        self.assertIn("is_correct", item["options"][1])
        self.assertTrue(item["options"][1]["is_correct"])
        self.assertEqual(item["correct_indexes"], [1])
        self.assertEqual(item["explanation"], "2+2=4")

    def test_get_question_unknown_returns_none(self):
        self.assertIsNone(tools.get_question(999999))
        self.assertIsNone(tools.get_question("abc"))

    def test_status_published_filter(self):
        draft = Question.objects.create(
            subject=self.math,
            text_uz="Qoralama savol",
            status=Question.Status.DRAFT,
            is_active=True,
        )
        self.assertNotIn("Qoralama savol", [q["text"] for q in tools.search_questions(limit=100)])