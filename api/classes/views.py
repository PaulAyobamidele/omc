from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import (
    SchoolClass, ClassSubject, ClassSubjectPermission,
    AcademicSession, Term,
)
from .serializers import (
    SchoolClassSerializer, ClassSubjectSerializer,
    AcademicSessionSerializer, TermSerializer,
)
from .permissions import IsAdminOrClassTeacher, CanManageClassSubject
from users.permissions import IsAdmin, IsAdminOrTeacher
from teachers.models import Teacher


class AcademicSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = AcademicSessionSerializer

    def get_queryset(self):
        return AcademicSession.objects.filter(school=self.request.school)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(school=self.request.school)


class TermListCreateView(generics.ListCreateAPIView):
    serializer_class = TermSerializer

    def get_queryset(self):
        qs = Term.objects.select_related("session").filter(
            session__school=self.request.school
        )
        session_id = self.request.query_params.get("session")
        if session_id:
            qs = qs.filter(session_id=session_id)
        active_only = self.request.query_params.get("active")
        if active_only:
            qs = qs.filter(is_active=True)
        return qs

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]


class ActiveTermView(generics.RetrieveAPIView):
    serializer_class = TermSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Term.objects.filter(
            session__school=self.request.school, is_active=True
        ).select_related("session").first()

    def get(self, request, *args, **kwargs):
        term = self.get_object()
        if not term:
            return Response({"detail": "No active term set."}, status=status.HTTP_404_NOT_FOUND)
        return Response(TermSerializer(term).data)


class SchoolClassListCreateView(generics.ListCreateAPIView):
    serializer_class = SchoolClassSerializer

    def get_queryset(self):
        return SchoolClass.objects.select_related("class_teacher__user").filter(
            school=self.request.school
        )

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(school=self.request.school)


class SchoolClassRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated, IsAdminOrClassTeacher]

    def get_queryset(self):
        return SchoolClass.objects.filter(school=self.request.school)


class ClassSubjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ClassSubjectSerializer

    def get_queryset(self):
        from django.db.models import Q
        qs = ClassSubject.objects.select_related(
            "school_class", "subject", "teacher__user"
        ).filter(school_class__school=self.request.school)

        user = self.request.user
        if user.role == "teacher":
            teacher = user.teacher_profile
            managed_class_ids = teacher.classes_managed.values_list("id", flat=True)
            qs = qs.filter(
                Q(teacher=teacher) |
                Q(school_class_id__in=managed_class_ids) |
                Q(permissions__teacher=teacher, permissions__can_enter_grades=True)
            ).distinct()

        class_id = self.request.query_params.get("class_id")
        if class_id:
            qs = qs.filter(school_class_id=class_id)
        return qs

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdminOrTeacher()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        school_class = serializer.validated_data["school_class"]
        user = self.request.user

        if user.role == "admin":
            serializer.save()
        elif user.role == "teacher":
            teacher = user.teacher_profile
            if school_class.class_teacher == teacher:
                serializer.save()
            else:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Only the class teacher or an admin can assign subjects.")
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission for this action.")


class ClassSubjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassSubjectSerializer
    permission_classes = [IsAuthenticated, CanManageClassSubject]

    def get_queryset(self):
        return ClassSubject.objects.filter(school_class__school=self.request.school)


class AssignClassSubjectPermissionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def post(self, request, *args, **kwargs):
        class_subject_id = request.data.get("class_subject")
        teacher_id = request.data.get("teacher")

        if not class_subject_id or not teacher_id:
            return Response(
                {"detail": "Both class_subject and teacher are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            class_subject = ClassSubject.objects.select_related("school_class").get(
                id=class_subject_id, school_class__school=request.school
            )
        except ClassSubject.DoesNotExist:
            return Response({"detail": "ClassSubject not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == "teacher":
            teacher_profile = request.user.teacher_profile
            if class_subject.school_class.class_teacher != teacher_profile:
                return Response(
                    {"detail": "Only the class teacher can assign grade permissions."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        try:
            teacher = Teacher.objects.get(id=teacher_id, user__school=request.school)
        except Teacher.DoesNotExist:
            return Response({"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

        perm, created = ClassSubjectPermission.objects.get_or_create(
            class_subject=class_subject,
            teacher=teacher,
            defaults={"can_enter_grades": True},
        )
        if not created:
            perm.can_enter_grades = True
            perm.save()

        return Response(
            {"detail": f"Permission granted to {teacher.user.get_full_name()} for {class_subject}"},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
