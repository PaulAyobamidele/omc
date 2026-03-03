from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Subject
from teachers.models import Teacher, TeacherSubjectAssignment
from .serializers import SubjectSerializer, SubjectDetailSerializer
from .permissions import IsAdminOrTeacher


class SubjectListCreateView(generics.ListCreateAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return Subject.objects.filter(school=self.request.school)

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsAdminOrTeacher()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(school=self.request.school)


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubjectDetailSerializer

    def get_queryset(self):
        return Subject.objects.filter(school=self.request.school)

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [permissions.IsAuthenticated(), IsAdminOrTeacher()]
        return [permissions.IsAuthenticated()]


class AssignTeacherToSubjectView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeacher]

    def post(self, request, *args, **kwargs):
        subject_id = request.data.get("subject_id")
        teacher_id = request.data.get("teacher_id")

        if not subject_id or not teacher_id:
            return Response(
                {"detail": "Both subject_id and teacher_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            subject = Subject.objects.get(id=subject_id, school=request.school)
        except Subject.DoesNotExist:
            return Response({"detail": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            teacher = Teacher.objects.get(id=teacher_id, user__school=request.school)
        except Teacher.DoesNotExist:
            return Response({"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

        assignment, created = TeacherSubjectAssignment.objects.get_or_create(
            subject=subject, teacher=teacher
        )

        return Response(
            {
                "detail": "Teacher assigned successfully." if created else "Assignment already exists.",
                "assignment_id": assignment.id,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
