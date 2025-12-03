from rest_framework.permissions import BasePermission
from classes.models import ClassSubject
from teachers.models import Teacher

# from rest_framework.permissions import BasePermission
from classes.models import ClassSubjectPermission

class IsSubjectTeacher(BasePermission):
    """
    Teacher must either be the assigned subject teacher for the class
    OR have explicit permission granted via ClassSubjectPermission.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'teacher_profile')

    def has_object_permission(self, request, view, obj):
        teacher = request.user.teacher_profile
        student_class = getattr(obj.student, 'school_class', None)
        if not student_class:
            return False

        # Check direct ClassSubject assignment
        direct_assignment = obj.subject.class_assignments.filter(
            school_class=student_class,
            teacher=teacher
        ).exists()

        # Check ClassSubjectPermission table
        permission = ClassSubjectPermission.objects.filter(
            class_subject__school_class=student_class,
            class_subject__subject=obj.subject,
            teacher=teacher,
            can_enter_grades=True
        ).exists()

        return direct_assignment or permission



class IsClassTeacher(BasePermission):
    """
    Allows access only if the user is the class teacher of the student's class.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'teacher_profile')

    def has_object_permission(self, request, view, obj):
        teacher = request.user.teacher_profile
        student_class = getattr(obj.student, 'school_class', None)
        if not student_class:
            return False
        return student_class.class_teacher == teacher


class CanEnterGradeForThisCategory(BasePermission):
    """
    Ensure the teacher can enter grade only for allowed categories.
    """
    allowed_categories = ['mid-term test', 'assignment 1', 'assignment 2', 'final examination']

    def has_permission(self, request, view):
        category = request.data.get('category')
        return category in self.allowed_categories
