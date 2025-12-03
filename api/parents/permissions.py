from rest_framework.permissions import BasePermission
from parents.models import Parent
from students.models import Student


class IsParentOfStudent(BasePermission):
    """
    Parent can only access their own children.
    """

    def has_permission(self, request, view):
        if request.user.role != "parent":
            return False

        parent = Parent.objects.filter(user=request.user).first()
        if not parent:
            return False

        student_id = view.kwargs.get("student_id") or request.data.get("student_id")

        if not student_id:
            return False

        return Student.objects.filter(
            id=student_id,
            parent=parent
        ).exists()
