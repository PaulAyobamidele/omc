from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher
from students.models import Student
from .models import Teacher
from rest_framework import status



class TeacherDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        teacher = Teacher.objects.get(user=request.user)
        data = {
            "message": f"Welcome to the teacher dashboard, {teacher.user.username}!",
            "teacher_id": teacher.id,
            "subjects": teacher.subjects,
        }
        return Response(data)
