from rest_framework.permissions import BasePermission


class IsAdminOrClassTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        teacher = getattr(request.user, "teacher_profile", None)
        if not teacher:
            return False
        return obj.class_teacher == teacher


class CanManageClassSubject(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ("admin", "teacher")

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        teacher = getattr(request.user, "teacher_profile", None)
        if not teacher:
            return False
        return obj.school_class.class_teacher == teacher
