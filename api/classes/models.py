from django.db import models
from teachers.models import Teacher
from subjects.models import Subject
# from classes.models import SchoolClass

# Create your models here.


class SchoolClass(models.Model):
    name = models.CharField(max_length=100)
    class_teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL,
        null = True,
        blank = True,
        related_name='classes_managed')

    def __str__(self):
        return self.name
    
    
class ClassSubject(models.Model):
    school_class = models.ForeignKey(
        SchoolClass, 
        on_delete=models.CASCADE,
        related_name='subjects')
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE,
        related_name='class_assignments')
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL,
        null = True,
        blank = True,
        related_name='class_subjects')

    class Meta:
        unique_together = ('school_class', 'subject')

    def __str__(self):
        return f"{self.school_class.name} - {self.subject.name} ({self.teacher.user.get_full_name() if self.teacher else 'No Teacher'})"
    
    
    
class ClassSubjectPermission(models.Model):
    """
    Tracks which teacher has permission to enter grades for a class-subject combination.
    Usually assigned by the class teacher.
    """
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, related_name='permissions')
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='subject_permissions')
    can_enter_grades = models.BooleanField(default=True)

    class Meta:
        unique_together = ('class_subject', 'teacher')

    def __str__(self):
        return f"{self.teacher.user.get_full_name()} -> {self.class_subject}"
