from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from users.permissions import IsTeacher, IsAdminOrTeacher
from .models import Teacher
from .serializers import TeacherSerializer


class TeacherDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        teacher = request.user.teacher_profile
        classes_managed = teacher.classes_managed.all()
        class_subjects = teacher.class_subjects.select_related(
            "school_class", "subject"
        ).all()

        return Response({
            "teacher_id": teacher.id,
            "name": request.user.get_full_name(),
            "classes_managed": [
                {"id": c.id, "name": c.name}
                for c in classes_managed
            ],
            "subjects_teaching": [
                {
                    "id": cs.id,
                    "class": cs.school_class.name,
                    "subject": cs.subject.name,
                }
                for cs in class_subjects
            ],
        })


class TeacherListView(generics.ListAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def get_queryset(self):
        return Teacher.objects.select_related("user").filter(
            user__school=self.request.school
        )
