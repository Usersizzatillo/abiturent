from io import StringIO

from django.contrib.auth import get_user_model
from django.test import TestCase

from catalog.models import Subject
from questions.importexport import export_csv, import_csv
from questions.models import Question, QuestionOption

User = get_user_model()

SAMPLE_CSV = (
    "subject,topic,text_uz,text_ru,question_type,difficulty,status,source_type,"
    "is_verified,explanation_uz,option1_uz,option1_correct,option2_uz,option2_correct\n"
    "matematika,Algebra,2+2 nechiga teng?,,single,1,published,dtm,true,4 ga teng,"
    "3,false,4,true\n"
)


class ImportExportTests(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name_uz="Matematika", slug="matematika")
        self.user = User.objects.create_user(username="teacher1", password="Passw0rd!")

    def test_import_creates_question_with_options(self):
        created, errors = import_csv(StringIO(SAMPLE_CSV))
        self.assertEqual(errors, [])
        self.assertEqual(created, 1)
        q = Question.objects.get()
        self.assertEqual(q.subject, self.subject)
        self.assertEqual(q.question_type, "single")
        self.assertEqual(q.difficulty, Question.Difficulty.EASY)
        self.assertEqual(q.status, Question.Status.PUBLISHED)
        self.assertEqual(q.source_type, Question.SourceType.DTM)
        self.assertTrue(q.is_verified)
        self.assertEqual(q.options.count(), 2)
        self.assertEqual(q.options.filter(is_correct=True).count(), 1)

    def test_import_records_created_by(self):
        csv_text = SAMPLE_CSV.replace("\nmatematika", "\nmatematika")
        created, errors = import_csv(StringIO(SAMPLE_CSV), created_by=self.user)
        self.assertEqual(errors, [])
        q = Question.objects.get()
        self.assertEqual(q.created_by, self.user)

    def test_import_rejects_missing_options(self):
        bad = (
            "subject,text_uz,option1_uz,option1_correct\n"
            "matematika,Xavfli savol,A,true\n"
        )
        created, errors = import_csv(StringIO(bad))
        self.assertEqual(created, 0)
        self.assertEqual(len(errors), 1)
        self.assertIn("2 ta variant", errors[0])

    def test_import_rejects_single_with_two_correct(self):
        bad = (
            "subject,text_uz,question_type,option1_uz,option1_correct,option2_uz,option2_correct\n"
            "matematika,Ikkala to'g'ri,single,A,true,B,true\n"
        )
        created, errors = import_csv(StringIO(bad))
        self.assertEqual(created, 0)
        self.assertIn("bitta to'g'ri javob", errors[0])

    def test_export_returns_header_and_rows(self):
        q = Question.objects.create(
            subject=self.subject,
            text_uz="2+2?",
            status=Question.Status.PUBLISHED,
            created_by=self.user,
        )
        QuestionOption.objects.create(question=q, text_uz="3", is_correct=False, sort_order=0)
        QuestionOption.objects.create(question=q, text_uz="4", is_correct=True, sort_order=1)

        text = export_csv(Question.objects.all())
        self.assertIn("subject,topic,text_uz", text)
        self.assertIn("2+2?", text)
        self.assertIn("option2_correct", text)

    def test_export_import_roundtrip(self):
        q = Question.objects.create(
            subject=self.subject, text_uz="1+1?", status=Question.Status.PUBLISHED
        )
        QuestionOption.objects.create(question=q, text_uz="2", is_correct=True, sort_order=0)
        QuestionOption.objects.create(question=q, text_uz="1", is_correct=False, sort_order=1)

        text = export_csv(Question.objects.all())
        before = Question.objects.count()
        created, errors = import_csv(StringIO(text))
        self.assertEqual(errors, [])
        self.assertEqual(created, 1)
        self.assertEqual(Question.objects.count(), before + 1)
        new_q = Question.objects.get(text_uz="1+1?", pk__gt=q.pk)
        self.assertEqual(new_q.options.filter(is_correct=True).count(), 1)