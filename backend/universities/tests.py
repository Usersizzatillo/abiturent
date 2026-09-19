from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Subject
from .models import Direction, University


class UniversityApiTests(APITestCase):
    def setUp(self):
        self.math = Subject.objects.create(name_uz="Matematika", slug="matematika", sort_order=0)
        self.uni = University.objects.create(
            name_uz="O'zbekiston Milliy universiteti",
            slug="numu",
            city_uz="Toshkent",
            established=1918,
            sort_order=0,
        )
        self.direction = Direction.objects.create(
            university=self.uni,
            name_uz="Matematika",
            code="mat",
            duration_years=4,
            sort_order=0,
        )
        self.direction.subjects.add(self.math)

    def test_list_universities(self):
        res = self.client.get("/api/universities/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["count"] >= 1)
        uni = next(u for u in res.data["results"] if u["slug"] == "numu")
        self.assertEqual(uni["direction_count"], 1)
        self.assertEqual(uni["name_uz"], "O'zbekiston Milliy universiteti")

    def test_detail_includes_directions(self):
        res = self.client.get("/api/universities/numu/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["directions"]), 1)
        direction = res.data["directions"][0]
        self.assertEqual(direction["code"], "mat")
        self.assertEqual(len(direction["subjects"]), 1)
        self.assertEqual(direction["subjects"][0]["slug"], "matematika")
        self.assertEqual(direction["university"]["slug"], "numu")

    def test_public_can_read_anonymous(self):
        res = self.client.get("/api/universities/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_directions_filter_by_subject(self):
        res = self.client.get(f"/api/directions/?subject={self.math.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)

    def test_directions_filter_by_university_slug(self):
        res = self.client.get("/api/directions/?university=numu")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)

    def test_404_unknown_university(self):
        res = self.client.get("/api/universities/nonexistent/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)