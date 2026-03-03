from django.db import models
from teachers.models import Teacher
from subjects.models import Subject
from common.models import SchoolOwnedModel


class AcademicSession(SchoolOwnedModel):
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]
        unique_together = [("school", "name")]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_active:
            AcademicSession.objects.filter(
                school=self.school, is_active=True
            ).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class Term(models.Model):
    TERM_CHOICES = [
        ("FIRST", "First Term"),
        ("SECOND", "Second Term"),
        ("THIRD", "Third Term"),
    ]

    session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, related_name="terms"
    )
    name = models.CharField(max_length=10, choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ("session", "name")
        ordering = ["session", "name"]

    def __str__(self):
        return f"{self.session.name} — {self.get_name_display()}"

    def save(self, *args, **kwargs):
        if self.is_active:
            Term.objects.filter(
                session__school=self.session.school, is_active=True
            ).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class SchoolClass(SchoolOwnedModel):
    name = models.CharField(max_length=100)
    class_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classes_managed",
    )

    class Meta:
        verbose_name_plural = "School Classes"

    def __str__(self):
        return self.name


class ClassSubject(models.Model):
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, related_name="subjects"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="class_assignments"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="class_subjects",
    )

    class Meta:
        unique_together = ("school_class", "subject")

    def __str__(self):
        teacher_name = self.teacher.user.get_full_name() if self.teacher else "No Teacher"
        return f"{self.school_class.name} — {self.subject.name} ({teacher_name})"


class ClassSubjectPermission(models.Model):
    class_subject = models.ForeignKey(
        ClassSubject, on_delete=models.CASCADE, related_name="permissions"
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="subject_permissions"
    )
    can_enter_grades = models.BooleanField(default=True)

    class Meta:
        unique_together = ("class_subject", "teacher")

    def __str__(self):
        return f"{self.teacher.user.get_full_name()} → {self.class_subject}"
