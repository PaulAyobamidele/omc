from rest_framework.permissions import BasePermission
from classes.models import ClassSubjectPermission


class CanEnterGrades(BasePermission):
    """
    Teacher can enter grades if they are EITHER:
    1. The assigned subject teacher for this class-subject, OR
    2. The class teacher, OR
    3. Have explicit ClassSubjectPermission granted
    """
    def has_permission(self, request, view):
        if not hasattr(request.user, "teacher_profile"):
            return False

        teacher = request.user.teacher_profile
        class_subject_id = request.data.get("class_subject")

        if not class_subject_id:
            return False

        from classes.models import ClassSubject
        try:
            cs = ClassSubject.objects.select_related("school_class", "teacher").get(id=class_subject_id)
        except ClassSubject.DoesNotExist:
            return False

        if cs.teacher == teacher:
            return True

        if cs.school_class.class_teacher == teacher:
            return True

        if ClassSubjectPermission.objects.filter(
            class_subject=cs, teacher=teacher, can_enter_grades=True
        ).exists():
            return True

        return False


class CanViewGrades(BasePermission):
    """
    Any authenticated user with a valid role can view grades
    (further filtering happens in the queryset).
    """
    def has_permission(self, request, view):
        return request.user.role in ("teacher", "student", "parent", "admin")
