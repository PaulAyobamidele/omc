from django.db import models
from django.conf import settings
from common.models import SchoolOwnedModel


class Parent(SchoolOwnedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parent_profile",
    )
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = [("school", "phone")]

    def __str__(self):
        return self.user.username
