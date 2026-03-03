from django.contrib import admin
from .models import GradeEntry

@admin.register(GradeEntry)
class GradeEntryAdmin(admin.ModelAdmin):
    list_display = ["student", "class_subject", "term", "category", "score", "teacher", "created_at"]
    list_filter = ["term", "category", "class_subject__subject"]
    search_fields = ["student__user__first_name", "student__user__last_name"]
