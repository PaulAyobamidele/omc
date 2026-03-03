from django.db import models
from django.conf import settings
from subjects.models import Subject


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["user__last_name", "user__first_name"]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class TeacherSubjectAssignment(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="subject_assignments",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="teacher_assignments",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("teacher", "subject")

    def __str__(self):
        return f"{self.teacher} → {self.subject}"
