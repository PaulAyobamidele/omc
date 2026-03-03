from django.db import models


class SchoolOwnedModel(models.Model):
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='+',
    )

    class Meta:
        abstract = True
