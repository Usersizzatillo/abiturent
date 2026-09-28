from django.test import TestCase, override_settings

from catalog.models import Subject, Subtopic, Topic
from questions.models import Question, QuestionOption
from universities.models import Direction, University

from . import tools
from .auth import (
    TIER_ADMIN,
    TIER_ANONYMOUS,
    TIER_READ,
    McpAuthError,
    authenticate,
    current_tier,
    is_configured,
    require_admin,
    set_tier,
)


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
        # The tool layer trusts the ambient tier (set by the auth middleware for
        # HTTP, or by the stdio transport for local runs).
        set_tier(TIER_ADMIN)

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

    def test_get_question_hides_draft(self):
        """Draft/archived questions are teacher work-in-progress and stay private."""
        draft = Question.objects.create(
            subject=self.math,
            text_uz="Yashirin qoralama",
            status=Question.Status.DRAFT,
            is_active=True,
        )
        QuestionOption.objects.create(
            question=draft, text_uz="A", is_correct=True, sort_order=0
        )
        QuestionOption.objects.create(
            question=draft, text_uz="B", is_correct=False, sort_order=1
        )
        self.assertIsNone(tools.get_question(draft.id))
        self.assertIsNone(tools.get_question(draft.id, include_answers=True))

    def test_get_question_published_without_answers(self):
        item = tools.get_question(self.q.id)
        self.assertIsNotNone(item)
        self.assertNotIn("is_correct", item["options"][0])
        self.assertNotIn("correct_indexes", item)
        self.assertNotIn("explanation", item)


@override_settings(MCP_API_KEY="read-key", MCP_ADMIN_API_KEY="admin-key")
class McpAuthTests(TestCase):
    """The bridge serves the answer key, so it must fail closed without a key."""

    def setUp(self):
        self.subject = Subject.objects.create(name_uz="Matematika", slug="matematika")
        self.q = Question.objects.create(
            subject=self.subject,
            text_uz="2+2?",
            status=Question.Status.PUBLISHED,
            is_active=True,
        )
        QuestionOption.objects.create(
            question=self.q, text_uz="3", is_correct=False, sort_order=0
        )
        QuestionOption.objects.create(
            question=self.q, text_uz="4", is_correct=True, sort_order=1
        )
        set_tier(TIER_ANONYMOUS)

    def test_authenticate_maps_tokens_to_tiers(self):
        self.assertEqual(authenticate("admin-key"), TIER_ADMIN)
        self.assertEqual(authenticate("read-key"), TIER_READ)
        self.assertEqual(authenticate("nope"), TIER_ANONYMOUS)
        self.assertEqual(authenticate(""), TIER_ANONYMOUS)
        # A read key must not be accepted as an admin key.
        self.assertNotEqual(authenticate("read-key"), TIER_ADMIN)

    def test_is_configured(self):
        self.assertTrue(is_configured())

    @override_settings(MCP_API_KEY="", MCP_ADMIN_API_KEY="")
    def test_is_configured_fails_closed(self):
        self.assertFalse(is_configured())

    def test_require_admin_blocks_non_admin(self):
        set_tier(TIER_READ)
        with self.assertRaises(McpAuthError):
            require_admin("include_answers")
        set_tier(TIER_ADMIN)
        require_admin("include_answers")

    def test_search_questions_include_answers_requires_admin(self):
        set_tier(TIER_READ)
        with self.assertRaises(McpAuthError):
            tools.search_questions(subject_slug="matematika", include_answers=True)
        set_tier(TIER_ADMIN)
        res = tools.search_questions(subject_slug="matematika", include_answers=True)
        self.assertTrue(res[0]["options"][1]["is_correct"])

    def test_get_question_include_answers_requires_admin(self):
        set_tier(TIER_READ)
        with self.assertRaises(McpAuthError):
            tools.get_question(self.q.id, include_answers=True)
        set_tier(TIER_ADMIN)
        item = tools.get_question(self.q.id, include_answers=True)
        self.assertEqual(item["correct_indexes"], [1])

    def test_read_tier_never_leaks_answers(self):
        set_tier(TIER_READ)
        for item in tools.search_questions(limit=10):
            for option in item["options"]:
                self.assertNotIn("is_correct", option)
            self.assertNotIn("correct_indexes", item)
            self.assertNotIn("explanation", item)
        item = tools.get_question(self.q.id)
        for option in item["options"]:
            self.assertNotIn("is_correct", option)


class McpAuthMiddlewareTests(TestCase):
    """ASGI-level gate: unauthenticated callers cannot even list tools."""

    async def _request(self, headers):
        from .auth import BearerAuthMiddleware

        seen = {}

        async def app(scope, receive, send):
            seen["called"] = True
            seen["tier"] = current_tier()
            await send(
                {
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [(b"content-type", b"text/plain")],
                }
            )
            await send({"type": "http.response.body", "body": b"ok"})

        middleware = BearerAuthMiddleware(app)
        sent = []

        async def send(message):
            sent.append(message)

        async def receive():
            return {"type": "http.request"}

        await middleware({"type": "http", "path": "/mcp/", "headers": headers}, receive, send)
        starts = [m for m in sent if m["type"] == "http.response.start"]
        status = starts[0]["status"] if starts else 0
        return status, seen

    @override_settings(MCP_API_KEY="read-key", MCP_ADMIN_API_KEY="admin-key")
    async def test_missing_token_rejected(self):
        status, seen = await self._request([])
        self.assertEqual(status, 401)
        self.assertNotIn("called", seen)

    @override_settings(MCP_API_KEY="read-key", MCP_ADMIN_API_KEY="admin-key")
    async def test_invalid_token_rejected(self):
        status, seen = await self._request([(b"authorization", b"Bearer wrong")])
        self.assertEqual(status, 401)
        self.assertNotIn("called", seen)

    @override_settings(MCP_API_KEY="read-key", MCP_ADMIN_API_KEY="admin-key")
    async def test_non_bearer_scheme_rejected(self):
        status, _ = await self._request([(b"authorization", b"Basic read-key")])
        self.assertEqual(status, 401)

    @override_settings(MCP_API_KEY="read-key", MCP_ADMIN_API_KEY="admin-key")
    async def test_read_key_allowed(self):
        status, seen = await self._request([(b"authorization", b"Bearer read-key")])
        self.assertEqual(status, 200)
        self.assertTrue(seen["called"])
        self.assertEqual(seen["tier"], TIER_READ)

    @override_settings(MCP_API_KEY="read-key", MCP_ADMIN_API_KEY="admin-key")
    async def test_admin_key_allowed(self):
        status, seen = await self._request([(b"authorization", b"Bearer admin-key")])
        self.assertEqual(status, 200)
        self.assertEqual(seen["tier"], TIER_ADMIN)

    @override_settings(MCP_API_KEY="", MCP_ADMIN_API_KEY="")
    async def test_unconfigured_fails_closed(self):
        status, seen = await self._request([(b"authorization", b"Bearer anything")])
        self.assertEqual(status, 503)
        self.assertNotIn("called", seen)