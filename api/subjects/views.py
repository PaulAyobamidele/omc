from rest_framework import generics, permissions
from teachers.models import Subject, TeacherSubjectAssignment, Teacher
from .serializers import SubjectSerializer, SubjectDetailSerializer
from .permissions import IsAdminOrTeacher
from rest_framework.response import Response

class SubjectListView(generics.ListAPIView):
    """
    List all subjects.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubjectDetailView(generics.RetrieveAPIView):
    """
    Retrieve a subject with teachers and students.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class AssignTeacherToSubjectView(generics.CreateAPIView):
    """
    Assign a teacher to a subject.
    Only admins or class teachers can do this.
    """
    serializer_class = SubjectDetailSerializer  # Can create a minimal serializer if needed
    permission_classes = [IsAdminOrTeacher]

    def post(self, request, *args, **kwargs):
        subject_id = request.data.get('subject_id')
        teacher_id = request.data.get('teacher_id')

        try:
            subject = Subject.objects.get(id=subject_id)
            teacher = Teacher.objects.get(id=teacher_id)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=404)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=404)

        assignment, created = TeacherSubjectAssignment.objects.get_or_create(
            subject=subject,
            teacher=teacher
        )
        return Response({
            "message": "Teacher assigned successfully",
            "assignment_id": assignment.id
        })
