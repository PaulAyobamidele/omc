from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from grades.models import GradeEntry
from students.models import Student
from classes.models import Term


class StudentReportJSON(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        user = request.user

        if user.role == "parent":
            parent = getattr(user, "parent_profile", None)
            if not parent or not parent.students.filter(id=student_id).exists():
                return Response(
                    {"detail": "You do not have permission to view this report."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        elif user.role == "teacher":
            teacher = getattr(user, "teacher_profile", None)
            if not teacher:
                return Response(
                    {"detail": "Teacher profile not found."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            teaches_student = GradeEntry.objects.filter(
                student=student, teacher=teacher
            ).exists()
            manages_class = (
                student.school_class
                and student.school_class.class_teacher == teacher
            )
            if not (teaches_student or manages_class):
                return Response(
                    {"detail": "You do not have permission to view this report."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        elif user.role == "student":
            if user.student_profile.id != student_id:
                return Response(
                    {"detail": "You can only view your own report."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        elif user.role != "admin":
            return Response(
                {"detail": "Insufficient permissions."},
                status=status.HTTP_403_FORBIDDEN,
            )

        term_id = request.query_params.get("term")
        qs = GradeEntry.objects.filter(student=student).select_related(
            "class_subject__subject",
            "teacher__user",
            "term__session",
        )

        if term_id:
            qs = qs.filter(term_id=term_id)

        if not qs.exists():
            return Response(
                {"detail": "No grades found for this student."},
                status=status.HTTP_404_NOT_FOUND,
            )

        term = qs.first().term
        subjects_map = {}

        for g in qs:
            sid = g.class_subject.subject.id

            if sid not in subjects_map:
                subjects_map[sid] = {
                    "subject_id": sid,
                    "subject_name": g.class_subject.subject.name,
                    "teacher_name": g.teacher.user.get_full_name() if g.teacher else None,
                    "grades": [],
                    "total_score": 0,
                    "total_max": 0,
                }

            max_score = g.max_score
            percentage = round((float(g.score) / max_score * 100), 2) if max_score else 0

            subjects_map[sid]["grades"].append({
                "category": g.category,
                "category_display": g.get_category_display(),
                "score": float(g.score),
                "max_score": max_score,
                "percentage": percentage,
            })

            subjects_map[sid]["total_score"] += float(g.score)
            subjects_map[sid]["total_max"] += max_score

        subject_reports = []
        for data in subjects_map.values():
            data["percentage"] = round(
                (data["total_score"] / data["total_max"] * 100) if data["total_max"] > 0 else 0,
                2,
            )
            subject_reports.append(data)

        percentages = [s["percentage"] for s in subject_reports]
        overall = round(sum(percentages) / len(percentages), 2) if percentages else 0

        return Response({
            "student": {
                "id": student.id,
                "name": student.user.get_full_name(),
                "class": student.school_class.name if student.school_class else "Unassigned",
            },
            "term": str(term),
            "session": term.session.name if term else "N/A",
            "subjects": subject_reports,
            "overall_percentage": overall,
        })
