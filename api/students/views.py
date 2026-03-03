from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from .serializers import CreateStudentSerializer, StudentListSerializer
from .models import Student
from users.permissions import IsAdminOrTeacher


class CreateStudentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role not in ("parent", "teacher", "admin"):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CreateStudentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)


class StudentListView(generics.ListAPIView):
    serializer_class = StudentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        school = self.request.school
        qs = Student.objects.select_related(
            "user", "school_class", "parent__user"
        ).filter(school_class__school=school)

        if user.role == "parent":
            return qs.filter(parent=user.parent_profile)

        elif user.role == "teacher":
            teacher = user.teacher_profile
            managed_class_ids = teacher.classes_managed.values_list("id", flat=True)
            teaching_class_ids = teacher.class_subjects.values_list("school_class_id", flat=True)
            all_class_ids = set(managed_class_ids) | set(teaching_class_ids)
            return qs.filter(school_class_id__in=all_class_ids)

        elif user.role == "admin":
            return qs

        return Student.objects.none()


class StudentsByClassView(generics.ListAPIView):
    serializer_class = StudentListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def get_queryset(self):
        class_id = self.kwargs.get("class_id")
        return Student.objects.filter(
            school_class_id=class_id,
            school_class__school=self.request.school,
        ).select_related("user", "school_class", "parent__user")
