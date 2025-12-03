from django.db import models
from django.conf import settings


class Subject(models.Model):
    """
    A school subject (Mathematics, English, Physics, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """
    A teacher is a user with a role=teacher.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class TeacherSubjectAssignment(models.Model):
    """
    A teacher may be assigned to one or more subjects.
    This replaces Teacher.subjects ManyToManyField for more control.
    """
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="subject_assignments"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="teacher_assignments"
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('teacher', 'subject')
        verbose_name = "Teacher Subject Assignment"
        verbose_name_plural = "Teacher Subject Assignments"

    def __str__(self):
        return f"{self.teacher} → {self.subject}"
