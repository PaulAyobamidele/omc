# grades/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import GradeEntry
from classes.models import ClassSubject, SchoolClass
from teachers.models import Subject
from .serializers import GradeEntrySerializer
from .permissions import IsSubjectTeacher, IsClassTeacher, CanEnterGradeForThisCategory
from users.permissions import IsParent
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Sum
from .serializers import StudentSummarySerializer

class GradeEntryCreateView(generics.CreateAPIView):
    """
    Teachers enter grades for a student in a specific category.
    Permissions:
        - Must be assigned subject teacher
        - Must be class teacher or have permission from class teacher
        - Must use a valid grade category
    """
    queryset = GradeEntry.objects.all()
    serializer_class = GradeEntrySerializer
    permission_classes = [IsAuthenticated, IsSubjectTeacher, IsClassTeacher, CanEnterGradeForThisCategory]


class StudentGradesView(generics.ListAPIView):
    """
    Students can view all their grades for the current term.
    """
    serializer_class = GradeEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != "student":
            return GradeEntry.objects.none()
        # Optional: filter by current term
        current_term = self.request.query_params.get('term')
        qs = GradeEntry.objects.filter(student=user.student_profile)
        if current_term:
            qs = qs.filter(term=current_term)
        return qs


class ParentGradesView(generics.ListAPIView):
    """
    Parents can view grades for their children only.
    """
    serializer_class = GradeEntrySerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        user = self.request.user
        children = user.parent_profile.students.all()
        current_term = self.request.query_params.get('term')
        qs = GradeEntry.objects.filter(student__in=children)
        if current_term:
            qs = qs.filter(term=current_term)
        return qs


class SubjectGradesView(generics.ListAPIView):
    """
    Teacher can see all grades for a subject they teach.
    """
    serializer_class = GradeEntrySerializer
    permission_classes = [IsAuthenticated, IsSubjectTeacher]

    def get_queryset(self):
        subject_id = self.kwargs.get("subject_id")
        teacher_profile = self.request.user.teacher_profile

        if not teacher_profile.subjects.filter(id=subject_id).exists():
            raise PermissionDenied("You are not assigned to this subject.")

        current_term = self.request.query_params.get('term')
        qs = GradeEntry.objects.filter(subject_id=subject_id)
        if current_term:
            qs = qs.filter(term=current_term)
        return qs


class ClassGradesView(generics.ListAPIView):
    """
    Class teacher can view all grades for their class.
    """
    serializer_class = GradeEntrySerializer
    permission_classes = [IsAuthenticated, IsClassTeacher]

    def get_queryset(self):
        class_id = self.kwargs.get("class_id")
        teacher_profile = self.request.user.teacher_profile

        # Check if teacher is assigned to this class
        if not teacher_profile.classes.filter(id=class_id).exists():
            raise PermissionDenied("You are not assigned to this class.")

        current_term = self.request.query_params.get('term')
        qs = GradeEntry.objects.filter(student__school_class_id=class_id)
        if current_term:
            qs = qs.filter(term=current_term)
        return qs


class StudentSubjectGradesView(generics.ListAPIView):
    """
    Teacher or student can view grades for a specific student in a subject.
    """
    serializer_class = GradeEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")
        subject_id = self.kwargs.get("subject_id")
        user = self.request.user

        # Students can only view themselves
        if user.role == "student" and user.student_profile.id != student_id:
            return GradeEntry.objects.none()

        # Teachers must teach the subject or be class teacher
        if user.role == "teacher":
            teacher_profile = user.teacher_profile
            subject_check = teacher_profile.subjects.filter(id=subject_id).exists()
            class_check = teacher_profile.classes.filter(students__id=student_id).exists()
            if not (subject_check or class_check):
                raise PermissionDenied("You cannot view grades for this student in this subject.")

        current_term = self.request.query_params.get('term')
        qs = GradeEntry.objects.filter(student_id=student_id, subject_id=subject_id)
        if current_term:
            qs = qs.filter(term=current_term)
        return qs


class StudentGradeSummaryView(APIView):
    """ /grades/student/{student_id}/summary/ """
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        grades = GradeEntry.objects.filter(student_id=student_id)
        if not grades.exists():
            return Response({"detail": "No grades found"}, status=404)

        subjects = []
        overall_total = 0
        overall_count = 0

        # aggregate per subject
        subject_groups = grades.values('class_subject__subject__id', 'class_subject__subject__name').annotate(
            total_score=Sum('score'),
            average_score=Avg('score')
        )

        for g in subject_groups:
            subjects.append({
                "subject_id": g['class_subject__subject__id'],
                "subject_name": g['class_subject__subject__name'],
                "total_score": float(g['total_score']),
                "average_score": float(g['average_score']),
                "percentage": float(g['average_score'])  # adjust if needed
            })
            overall_total += g['total_score']
            overall_count += 1

        overall_average = overall_total / overall_count if overall_count else 0

        data = {
            "student_id": student_id,
            "student_name": grades.first().student.user.get_full_name(),
            "subjects": subjects,
            "overall_total": float(overall_total),
            "overall_average": float(overall_average),
            "overall_percentage": float(overall_average)
        }

        return Response(StudentSummarySerializer(data).data)


class ClassGradeSummaryView(APIView):
    """ /grades/class/{class_id}/summary/ """
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id):
        students = GradeEntry.objects.filter(student__school_class_id=class_id).values('student').distinct()
        result = []

        for s in students:
            grades = GradeEntry.objects.filter(student_id=s['student'], student__school_class_id=class_id)
            student_name = grades.first().student.user.get_full_name() if grades.exists() else ""
            subject_groups = grades.values('class_subject__subject__id', 'class_subject__subject__name').annotate(
                total_score=Sum('score'),
                average_score=Avg('score')
            )
            subjects = []
            overall_total = 0
            for g in subject_groups:
                subjects.append({
                    "subject_id": g['class_subject__subject__id'],
                    "subject_name": g['class_subject__subject__name'],
                    "total_score": float(g['total_score']),
                    "average_score": float(g['average_score']),
                    "percentage": float(g['average_score'])
                })
                overall_total += g['total_score']
            overall_average = overall_total / len(subject_groups) if subject_groups else 0
            result.append({
                "student_id": s['student'],
                "student_name": student_name,
                "subjects": subjects,
                "overall_total": float(overall_total),
                "overall_average": float(overall_average),
                "overall_percentage": float(overall_average)
            })

        return Response(result)


class SubjectGradeSummaryView(APIView):
    """ /grades/subject/{subject_id}/summary/ """
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        students = GradeEntry.objects.filter(class_subject__subject_id=subject_id).values('student').distinct()
        result = []

        for s in students:
            grades = GradeEntry.objects.filter(student_id=s['student'], class_subject__subject_id=subject_id)
            total_score = grades.aggregate(total=Sum('score'))['total'] or 0
            average_score = grades.aggregate(avg=Avg('score'))['avg'] or 0
            student_name = grades.first().student.user.get_full_name() if grades.exists() else ""
            result.append({
                "student_id": s['student'],
                "student_name": student_name,
                "subjects": [{
                    "subject_id": subject_id,
                    "subject_name": grades.first().class_subject.subject.name if grades.exists() else "",
                    "total_score": float(total_score),
                    "average_score": float(average_score),
                    "percentage": float(average_score)
                }],
                "overall_total": float(total_score),
                "overall_average": float(average_score),
                "overall_percentage": float(average_score)
            })
        return Response(result)
