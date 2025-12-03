from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import SchoolClass, ClassSubject, ClassSubjectPermission
from .serializers import SchoolClassSerializer, ClassSubjectSerializer
from .permissions import IsAdminOrClassTeacher, CanAssignTeacherToClassSubject
from teachers.models import Teacher
from rest_framework.response import Response
from rest_framework import status
# --- SchoolClass Views ---

class SchoolClassListCreateView(generics.ListCreateAPIView):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated]

class SchoolClassRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated, IsAdminOrClassTeacher]

# --- ClassSubject Views ---

class ClassSubjectListCreateView(generics.ListCreateAPIView):
    queryset = ClassSubject.objects.all()
    serializer_class = ClassSubjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Only allow admin or class teacher of the class to assign
        school_class = serializer.validated_data['school_class']
        if self.request.user.role == "admin":
            serializer.save()
        elif hasattr(self.request.user, "teacher_profile") and school_class.class_teacher == self.request.user.teacher_profile:
            serializer.save()
        else:
            raise PermissionError("You do not have permission to assign a teacher to this class.")

class ClassSubjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassSubject.objects.all()
    serializer_class = ClassSubjectSerializer
    permission_classes = [IsAuthenticated, CanAssignTeacherToClassSubject]





class AssignClassSubjectPermissionView(generics.CreateAPIView):
    """
    Class teacher assigns a teacher permission to enter grades for a specific class-subject.
    """
    permission_classes = [permissions.IsAuthenticated]  # Could add IsClassTeacher for extra safety

    def post(self, request, *args, **kwargs):
        class_subject_id = request.data.get('class_subject')
        teacher_id = request.data.get('teacher')

        try:
            class_subject = ClassSubject.objects.get(id=class_subject_id)
            teacher = Teacher.objects.get(id=teacher_id)
        except (ClassSubject.DoesNotExist, Teacher.DoesNotExist):
            return Response({"detail": "Invalid class_subject or teacher."}, status=status.HTTP_400_BAD_REQUEST)

        perm, created = ClassSubjectPermission.objects.get_or_create(
            class_subject=class_subject,
            teacher=teacher,
            defaults={'can_enter_grades': True}
        )
        if not created:
            perm.can_enter_grades = True
            perm.save()

        return Response({"detail": f"Permission granted to {teacher.user.get_full_name()} for {class_subject}"})
