from django.db import models
from students.models import Student
from teachers.models import Teacher
from teachers.models import Subject


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='grades_given')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return f"Grade {self.score} for {self.student.user.first_name} in {self.subject.name} by {self.teacher.user.first_name}"
    
    
