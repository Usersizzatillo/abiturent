from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import User


class AuthApiTests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.csrf_url = "/api/auth/csrf/"

    def _csrf_token(self):
        self.client.get(self.csrf_url)
        return self.client.cookies["csrftoken"].value

    def _post(self, path, data):
        token = self._csrf_token()
        return self.client.post(
            path, data, format="json", HTTP_X_CSRFTOKEN=token
        )

    def test_register_and_auto_login(self):
        res = self._post(
            "/api/auth/register/",
            {
                "username": "ali",
                "password": "StrongPass123!",
                "email": "ali@example.com",
                "role": "student",
            },
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="ali").exists())
        res = self.client.get("/api/auth/me/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["username"], "ali")

    def test_duplicate_username_rejected(self):
        User.objects.create_user(username="dupuser", password="x")
        res = self._post(
            "/api/auth/register/",
            {"username": "dupuser", "password": "StrongPass123!"},
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_and_logout_flow(self):
        User.objects.create_user(username="vali", password="StrongPass123!")
        res = self._post(
            "/api/auth/login/",
            {"username": "vali", "password": "StrongPass123!"},
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["username"], "vali")

        res = self.client.get("/api/auth/me/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self._post("/api/auth/logout/", {})
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.get("/api/auth/me/")
        self.assertIn(res.status_code, (401, 403))

    def test_login_wrong_password(self):
        User.objects.create_user(username="qayum", password="right-pass-1")
        res = self._post(
            "/api/auth/login/",
            {"username": "qayum", "password": "wrong-pass"},
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_requires_auth(self):
        res = self.client.get("/api/auth/me/")
        self.assertIn(res.status_code, (401, 403))

    def test_change_password(self):
        User.objects.create_user(username="soli", password="old-pass-1")
        self._post("/api/auth/login/", {"username": "soli", "password": "old-pass-1"})
        res = self._post(
            "/api/auth/change-password/",
            {"old_password": "old-pass-1", "new_password": "new-pass-1"},
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        self._post("/api/auth/logout/", {})
        res = self._post("/api/auth/login/", {"username": "soli", "password": "new-pass-1"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_teacher_role_only_via_admin(self):
        # An anonymous user cannot register as teacher through the public API.
        res = self._post(
            "/api/auth/register/",
            {"username": "teach", "password": "StrongPass123!", "role": "teacher"},
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_self_promote_role(self):
        User.objects.create_user(username="troll", password="StrongPass123!")
        self._post(
            "/api/auth/login/",
            {"username": "troll", "password": "StrongPass123!"},
        )
        token = self._csrf_token()
        res = self.client.patch(
            "/api/auth/me/",
            {"role": "admin"},
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        user = User.objects.get(username="troll")
        self.assertEqual(user.role, User.Role.STUDENT)