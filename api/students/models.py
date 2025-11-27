from django.db import models

# Create your models here.
from django.conf import settings
from parents.models import Parent

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='students')
    date_of_birth = models.DateField(blank=True, null=True)
    class_level = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        name = f"{self.user.first_name} {self.user.last_name}".strip()
        return name if name else self.user.username

