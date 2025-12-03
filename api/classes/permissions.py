from rest_framework.permissions import BasePermission

class IsAdminOrClassTeacher(BasePermission):
    """
    Allows access only to admins or the class teacher of the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        if hasattr(request.user, "teacher_profile"):
            teacher = request.user.teacher_profile
            return obj.class_teacher == teacher
        return False

class CanAssignTeacherToClassSubject(BasePermission):
    """
    Only admin or class teacher of the class can assign a teacher to a class-subject.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        if hasattr(request.user, "teacher_profile"):
            teacher = request.user.teacher_profile
            return obj.school_class.class_teacher == teacher
        return False
