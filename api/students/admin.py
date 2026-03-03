from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["user", "school_class", "parent", "date_of_birth"]
    list_filter = ["school_class"]
    search_fields = ["user__first_name", "user__last_name"]
