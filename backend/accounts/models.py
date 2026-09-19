from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user for the Abiturend platform."""

    class Role(models.TextChoices):
        STUDENT = "student", "Abituriyent"
        TEACHER = "teacher", "O'qituvchi"
        ADMIN = "admin", "Administrator"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        db_index=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    class Meta:
        db_table = "abiturend_user"