from rest_framework.permissions import BasePermission


class IsParentOfStudent(BasePermission):
    def has_permission(self, request, view):
        if request.user.role != "parent":
            return False

        parent = getattr(request.user, "parent_profile", None)
        if not parent:
            return False

        student_id = view.kwargs.get("student_id") or request.data.get("student_id")
        if not student_id:
            return False

        return parent.students.filter(id=student_id).exists()
