from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from grades.models import Grade
from students.models import Student
from users.models import User


class StudentReportJSON(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        user = request.user

        # --------------------------
        # Authorization
        # --------------------------
        if user.is_parent():
            parent_profile = getattr(user, "parent_profile", None)
            if parent_profile is None or student not in parent_profile.students.all():
                return Response({"detail": "You do not have permission to view this student's report."}, status=status.HTTP_403_FORBIDDEN)

        elif user.is_teacher():
            teacher_profile = getattr(user, "teacher_profile", None)
            if teacher_profile is None or not Grade.objects.filter(student=student, teacher=teacher_profile).exists():
                return Response({"detail": "You do not have permission to view this student's report."}, status=status.HTTP_403_FORBIDDEN)

        elif user.role == "admin":
            pass  # admins can view all

        else:
            return Response({"detail": "You do not have permission to view this student's report."}, status=status.HTTP_403_FORBIDDEN)

        # --------------------------
        # Gather grades
        # --------------------------
        grades_qs = Grade.objects.filter(student=student).select_related("teacher__user", "subject")
        grades = [
            {
                "subject": g.subject.name,
                "score": float(g.score),
                "teacher": g.teacher.user.get_full_name(),
                "comments": g.comments,
            }
            for g in grades_qs
        ]

        data = {
            "student": {
                "id": student.id,
                "first_name": student.user.first_name,
                "last_name": student.user.last_name,
                "class": student.class_level,
            },
            "grades": grades,
            "school": {
                "name": "Your School Name",
                "session": "2024/2025",
                "term": "First Term"
            }
        }

        return Response(data, status=status.HTTP_200_OK)
