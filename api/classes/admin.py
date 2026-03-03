from django.contrib import admin
from .models import SchoolClass, ClassSubject, ClassSubjectPermission, AcademicSession, Term

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "is_active"]

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ["session", "name", "start_date", "end_date", "is_active"]
    list_filter = ["session", "is_active"]

@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ["name", "class_teacher"]

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ["school_class", "subject", "teacher"]
    list_filter = ["school_class"]

@admin.register(ClassSubjectPermission)
class ClassSubjectPermissionAdmin(admin.ModelAdmin):
    list_display = ["class_subject", "teacher", "can_enter_grades"]
