# grades/models.py
from django.db import models
from students.models import Student
from teachers.models import Teacher
from classes.models import ClassSubject

class GradeEntry(models.Model):

    CATEGORY_CHOICES = [
        ('MIDTERM', 'Midterm Test'),
        ('ASSIGNMENT1', 'Assignment 1'),
        ('ASSIGNMENT2', 'Assignment 2'),
        ('EXAM', 'Final Exam'),
    ]

    CATEGORY_MAX_SCORES = {
        'MIDTERM': 20,
        'ASSIGNMENT1': 10,
        'ASSIGNMENT2': 10,
        'EXAM': 60,
    }

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    class_subject = models.ForeignKey(
        ClassSubject, on_delete=models.CASCADE, related_name="grade_entries"
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="grades_entered")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'class_subject', 'category')

    def __str__(self):
        return f"{self.student} - {self.class_subject.subject.name} ({self.category})"

    def clean(self):
        """Validate max score per category."""
        from django.core.exceptions import ValidationError
        max_score = self.CATEGORY_MAX_SCORES.get(self.category, 100)
        if self.score > max_score:
            raise ValidationError(f"{self.category} max score is {max_score}.")
