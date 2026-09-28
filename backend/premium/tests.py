from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Subject
from premium.models import Subscription, SubscriptionPlan
from questions.models import Question, QuestionOption

User = get_user_model()


class PremiumApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="student1", password="Passw0rd!", role=User.Role.STUDENT
        )
        self.free = SubscriptionPlan.objects.create(
            code="free-trial",
            tier=SubscriptionPlan.Tier.FREE,
            name_uz="Bepul",
            price_uzs=0,
            max_sessions_per_day=1,
        )
        self.pro = SubscriptionPlan.objects.create(
            code="pro-monthly",
            tier=SubscriptionPlan.Tier.PRO,
            name_uz="PRO",
            price_uzs=49_000,
            max_sessions_per_day=None,
        )
        self.subject = Subject.objects.create(name_uz="Matematika", slug="matematika")
        q = Question.objects.create(
            subject=self.subject, text_uz="2+2?", status=Question.Status.PUBLISHED
        )
        QuestionOption.objects.create(question=q, text_uz="4", is_correct=True, sort_order=0)
        QuestionOption.objects.create(question=q, text_uz="3", is_correct=False, sort_order=1)
        self.client.force_login(self.user)

    def _start(self):
        return self.client.post(
            "/api/sessions/",
            {"subject": self.subject.id, "question_count": 1, "mode": "practice"},
            format="json",
        )

    def test_plans_are_public(self):
        res = self.client.get("/api/premium/plans/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]["code"], "free-trial")

    def test_subscription_status_without_plan(self):
        res = self.client.get("/api/premium/subscription/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(res.data["is_premium"])
        self.assertIsNone(res.data["plan"])
        self.assertEqual(res.data["remaining_sessions_today"], 3)

    def test_subscribe_free_activates(self):
        res = self.client.post(
            "/api/premium/subscribe/", {"plan_code": "free-trial"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(res.data["is_premium"])
        self.assertTrue(res.data["plan"]["is_active"])

    def test_subscribe_paid_requires_gateway(self):
        res = self.client.post(
            "/api/premium/subscribe/", {"plan_code": "pro-monthly"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_402_PAYMENT_REQUIRED)

    def test_subscribe_unknown_plan_rejected(self):
        res = self.client.post(
            "/api/premium/subscribe/", {"plan_code": "nope"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_default_free_limit_blocks_session(self):
        for _ in range(3):
            res = self._start()
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res = self._start()
        self.assertEqual(res.status_code, status.HTTP_402_PAYMENT_REQUIRED)
        self.assertTrue(res.data["premium_required"])
        self.assertEqual(res.data["remaining_sessions_today"], 0)

    def test_subscribed_free_plan_applies_its_limit(self):
        self.client.post(
            "/api/premium/subscribe/", {"plan_code": "free-trial"}, format="json"
        )
        res = self._start()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res = self._start()
        self.assertEqual(res.status_code, status.HTTP_402_PAYMENT_REQUIRED)

    def test_premium_unlimited(self):
        Subscription.objects.create(
            user=self.user,
            plan=self.pro,
            starts_at=timezone.now(),
            ends_at=timezone.now() + timedelta(days=30),
        )
        for _ in range(5):
            res = self._start()
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_subscribe_extends_active_plan(self):
        Subscription.objects.create(
            user=self.user,
            plan=self.free,
            starts_at=timezone.now(),
            ends_at=timezone.now() + timedelta(days=5),
        )
        res = self.client.post(
            "/api/premium/subscribe/", {"plan_code": "free-trial"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        first = Subscription.objects.filter(user=self.user).order_by("created_at").first()
        latest = Subscription.objects.filter(user=self.user).order_by("-created_at").first()
        self.assertEqual(latest.starts_at, first.ends_at)