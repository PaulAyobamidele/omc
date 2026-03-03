from django.db import models
from django.conf import settings
from parents.models import Parent
from classes.models import SchoolClass


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    parent = models.ForeignKey(
        Parent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self):
        name = f"{self.user.first_name} {self.user.last_name}".strip()
        return name if name else self.user.username
