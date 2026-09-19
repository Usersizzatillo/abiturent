from django.test import SimpleTestCase
from django.urls import resolve

from rest_framework import status
from rest_framework.test import APITestCase

from core.views import API_ENDPOINTS


class ApiRootTests(APITestCase):
    def test_api_root_reports_endpoints(self):
        res = self.client.get("/api/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["version"], "1.0")
        self.assertGreater(len(res.data["endpoints"]), 10)

    def test_endpoint_catalog_is_in_sync_with_urlconf(self):
        """Every documented path must resolve; docs cannot rot silently."""
        for entry in API_ENDPOINTS:
            path = entry["path"]
            resolvable = path.replace("{slug}", "matematika").replace("{id}", "1")
            try:
                match = resolve(resolvable)
            except Exception as exc:  # noqa: BLE001 - assert message below
                self.fail(f"{path} no longer resolves: {exc}")

    def test_health_ok(self):
        res = self.client.get("/api/health/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["status"], "ok")


class SecurityHeadersTests(SimpleTestCase):
    def test_headers_present_on_api_response(self):
        res = self.client.get("/api/health/")
        self.assertEqual(res.headers["Referrer-Policy"], "strict-origin-when-cross-origin")
        self.assertIn("Permissions-Policy", res.headers)
        self.assertEqual(res.headers["X-Frame-Options"], "DENY")
        self.assertEqual(res.headers["X-Content-Type-Options"], "nosniff")