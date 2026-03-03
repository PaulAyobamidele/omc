from django.contrib import admin
from .models import Parent

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ["user", "phone"]
    search_fields = ["user__first_name", "user__last_name"]
