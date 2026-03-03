from django.db import models
from common.models import SchoolOwnedModel


class Subject(SchoolOwnedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["name"]
        unique_together = [("school", "name"), ("school", "code")]

    def __str__(self):
        return self.name
