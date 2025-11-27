from django.contrib.auth.models import AbstractUser

from django.db import models



class User(AbstractUser):
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length = 10, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    
    
    def is_parent(self):
        return self.role == 'parent'
    
    
    def is_student(self):
        return self.role == 'student'
    
    
    def is_teacher(self):
        return self.role == 'teacher'