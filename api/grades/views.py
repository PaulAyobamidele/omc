from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg

from .models import GradeEntry
from .serializers import GradeEntrySerializer, GradeEntryUpdateSerializer
from .permissions import CanEnterGrades, CanViewGrades
from users.permissions import IsParent
from classes.models import Term


GRADE_SELECT_RELATED = [
    "student__user", "student__school_class",
    "class_subject__subject", "class_subject__school_class",
    "teacher__user", "term__session",
]


def filter_by_term(queryset, request):
    term_id = request.query_params.get("term")
    if term_id:
        return queryset.filter(term_id=term_id)
    return queryset


class GradeEntryCreateView(generics.CreateAPIView):
    queryset = GradeEntry.objects.all()
    serializer_class = GradeEntrySerializer
    permission_classes = [IsAuthenticated, CanEnterGrades]


class GradeEntryUpdateView(generics.UpdateAPIView):
    serializer_class = GradeEntryUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GradeEntry.objects.filter(
            student__school_class__school=self.request.school
        )

    def get_object(self):
        obj = super().get_object()
        teacher = getattr(self.request.user, "teacher_profile", None)
        if not teacher or obj.teacher != teacher:
            raise PermissionDenied("You can only edit grades you entered.")
        return obj


class StudentGradesView(generics.ListAPIView):
    serializer_class = GradeEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != "student":
            return GradeEntry.objects.none()
        qs = GradeEntry.objects.filter(
            student=user.student_profile,
            student__school_class__school=self.request.school,
        ).select_related(*GRADE_SELECT_RELATED)
        return filter_by_term(qs, self.request)


class ParentGradesView(generics.ListAPIView):
    serializer_class = GradeEntrySerializer
    permission_classes = [IsAuthenticated, IsParent]

    def get_queryset(self):
        parent = self.request.user.parent_profile
        children_ids = parent.students.values_list("id", flat=True)
        qs = GradeEntry.objects.filter(
            student_id__in=children_ids,
            student__school_class__school=self.request.school,
        ).select_related(*GRADE_SELECT_RELATED)
        return filter_by_term(qs, self.request)


class ClassGradesView(generics.ListAPIView):
    serializer_class = GradeEntrySerializer
    permission_classes = [IsAuthenticated, CanViewGrades]

    def get_queryset(self):
        class_id = self.kwargs.get("class_id")
        user = self.request.user

        if user.role == "teacher":
            teacher = user.teacher_profile
            manages = teacher.classes_managed.filter(id=class_id).exists()
            teaches = teacher.class_subjects.filter(school_class_id=class_id).exists()
            if not (manages or teaches):
                raise PermissionDenied("You are not assigned to this class.")

        elif user.role not in ("admin",):
            raise PermissionDenied("You cannot view class grades.")

        qs = GradeEntry.objects.filter(
            student__school_class_id=class_id,
            student__school_class__school=self.request.school,
        ).select_related(*GRADE_SELECT_RELATED)
        return filter_by_term(qs, self.request)


class SubjectGradesView(generics.ListAPIView):
    serializer_class = GradeEntrySerializer
    permission_classes = [IsAuthenticated, CanViewGrades]

    def get_queryset(self):
        subject_id = self.kwargs.get("subject_id")
        user = self.request.user

        if user.role == "teacher":
            teacher = user.teacher_profile
            if not teacher.class_subjects.filter(subject_id=subject_id).exists():
                raise PermissionDenied("You are not assigned to teach this subject.")

        elif user.role not in ("admin",):
            raise PermissionDenied("You cannot view subject grades.")

        qs = GradeEntry.objects.filter(
            class_subject__subject_id=subject_id,
            student__school_class__school=self.request.school,
        ).select_related(*GRADE_SELECT_RELATED)
        return filter_by_term(qs, self.request)


class StudentGradeSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        user = request.user

        if user.role == "student" and user.student_profile.id != student_id:
            raise PermissionDenied("You can only view your own grades.")
        elif user.role == "parent":
            if not user.parent_profile.students.filter(id=student_id).exists():
                raise PermissionDenied("This is not your child.")

        qs = GradeEntry.objects.filter(
            student_id=student_id,
            student__school_class__school=request.school,
        ).select_related("class_subject__subject", "student__user")

        term_id = request.query_params.get("term")
        if term_id:
            qs = qs.filter(term_id=term_id)

        if not qs.exists():
            return Response({"detail": "No grades found."}, status=status.HTTP_404_NOT_FOUND)

        student = qs.first().student
        subjects = {}

        for entry in qs:
            sid = entry.class_subject.subject.id
            if sid not in subjects:
                subjects[sid] = {
                    "subject_id": sid,
                    "subject_name": entry.class_subject.subject.name,
                    "grades": [],
                    "total_score": 0,
                    "total_max": 0,
                }
            max_score = entry.max_score
            subjects[sid]["grades"].append({
                "category": entry.category,
                "category_display": entry.get_category_display(),
                "score": float(entry.score),
                "max_score": max_score,
            })
            subjects[sid]["total_score"] += float(entry.score)
            subjects[sid]["total_max"] += max_score

        subject_list = []
        for s in subjects.values():
            s["percentage"] = round(
                (s["total_score"] / s["total_max"] * 100) if s["total_max"] > 0 else 0, 2
            )
            subject_list.append(s)

        percentages = [s["percentage"] for s in subject_list]
        overall = round(sum(percentages) / len(percentages), 2) if percentages else 0

        return Response({
            "student_id": student_id,
            "student_name": student.user.get_full_name(),
            "subjects": subject_list,
            "overall_percentage": overall,
        })


class ClassGradeSummaryView(APIView):
    permission_classes = [IsAuthenticated, CanViewGrades]

    def get(self, request, class_id):
        user = request.user
        if user.role == "teacher":
            teacher = user.teacher_profile
            if not (teacher.classes_managed.filter(id=class_id).exists()
                    or teacher.class_subjects.filter(school_class_id=class_id).exists()):
                raise PermissionDenied("You are not assigned to this class.")
        elif user.role not in ("admin",):
            raise PermissionDenied("Insufficient permissions.")

        qs = GradeEntry.objects.filter(
            student__school_class_id=class_id,
            student__school_class__school=request.school,
        ).select_related("student__user", "class_subject__subject")

        term_id = request.query_params.get("term")
        if term_id:
            qs = qs.filter(term_id=term_id)

        students_data = {}
        for entry in qs:
            sid = entry.student_id
            if sid not in students_data:
                students_data[sid] = {
                    "student_id": sid,
                    "student_name": entry.student.user.get_full_name(),
                    "subjects": {},
                    "total_score": 0,
                    "total_max": 0,
                }

            subj_id = entry.class_subject.subject.id
            if subj_id not in students_data[sid]["subjects"]:
                students_data[sid]["subjects"][subj_id] = {
                    "subject_name": entry.class_subject.subject.name,
                    "total_score": 0,
                    "total_max": 0,
                }

            max_score = entry.max_score
            students_data[sid]["subjects"][subj_id]["total_score"] += float(entry.score)
            students_data[sid]["subjects"][subj_id]["total_max"] += max_score
            students_data[sid]["total_score"] += float(entry.score)
            students_data[sid]["total_max"] += max_score

        result = []
        for s in students_data.values():
            subject_list = []
            for subj in s["subjects"].values():
                subj["percentage"] = round(
                    (subj["total_score"] / subj["total_max"] * 100) if subj["total_max"] > 0 else 0, 2
                )
                subject_list.append(subj)

            s["subjects"] = subject_list
            s["overall_percentage"] = round(
                (s["total_score"] / s["total_max"] * 100) if s["total_max"] > 0 else 0, 2
            )
            result.append(s)

        result.sort(key=lambda x: x["overall_percentage"], reverse=True)

        return Response(result)
