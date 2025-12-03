from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from grades.models import GradeEntry as Grade
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
                return Response({"detail": "You do not have permission to view this student's report."},
                                status=status.HTTP_403_FORBIDDEN)

        elif user.is_teacher():
            teacher_profile = getattr(user, "teacher_profile", None)
            teaches_this_student = Grade.objects.filter(student=student, teacher=teacher_profile).exists()

            if teacher_profile is None or not teaches_this_student:
                return Response({"detail": "You do not have permission to view this student's report."},
                                status=status.HTTP_403_FORBIDDEN)

        elif user.role == "admin":
            pass  # admins can view all

        else:
            return Response({"detail": "You do not have permission to view this student's report."},
                            status=status.HTTP_403_FORBIDDEN)

        # --------------------------
        # Build Report Structure
        # --------------------------
        grade_entries = Grade.objects.filter(student=student).select_related(
            "teacher__user", "subject"
        )

        subjects_map = {}

        for g in grade_entries:
            sid = g.subject.id

            if sid not in subjects_map:
                subjects_map[sid] = {
                    "subject_id": sid,
                    "subject_name": g.subject.name,
                    "teacher_name": g.teacher.user.get_full_name() if g.teacher else None,
                    "grades": [],
                    "total_score": 0,
                    "total_maximum": 0,
                }

            percentage = round((g.score / g.maximum) * 100, 2) if g.maximum else 0

            subjects_map[sid]["grades"].append({
                "category": g.category,
                "score": float(g.score),
                "maximum": float(g.maximum),
                "percentage": percentage,
                "comments": g.comments,
            })

            subjects_map[sid]["total_score"] += g.score
            subjects_map[sid]["total_maximum"] += g.maximum

        # Compute subject averages
        subject_reports = []
        for sid, data in subjects_map.items():
            if data["total_maximum"] > 0:
                avg = round((data["total_score"] / data["total_maximum"]) * 100, 2)
            else:
                avg = 0.0

            data["average_percentage"] = avg
            subject_reports.append(data)

        # Compute overall student average
        percentages = [s["average_percentage"] for s in subject_reports]
        overall_average = round(sum(percentages) / len(percentages), 2) if percentages else 0.0

        # --------------------------
        # Final JSON Response
        # --------------------------
        data = {
            "student": {
                "id": student.id,
                "first_name": student.user.first_name,
                "last_name": student.user.last_name,
                "class": student.class_level,
            },
            "subjects": subject_reports,
            "overall_average": overall_average,
            "school": {
                "name": "Your School Name",
                "session": "2024/2025",
                "term": "First Term"
            }
        }

        return Response(data, status=status.HTTP_200_OK)
