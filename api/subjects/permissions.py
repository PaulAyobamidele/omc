from rest_framework.permissions import BasePermission

class IsAdminOrTeacher(BasePermission):
    """
    Allows access to admin or teacher users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'teacher']
