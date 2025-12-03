from django.db import models

# Create your models here.
class Subject (models.Model):
    name = models.CharField (max_length=100, unique=True)
    code = models.CharField (max_length=10, unique=True, blank=True, null=True)
    
    
    def __str__(self):
        return self.name
    
    
