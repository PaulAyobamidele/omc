from rest_framework import serializers
from .models import Subject
from teachers.models import TeacherSubjectAssignment


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name", "code", "description"]


class SubjectDetailSerializer(serializers.ModelSerializer):
    teachers = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ["id", "name", "code", "description", "teachers", "student_count"]

    def get_teachers(self, obj):
        assignments = TeacherSubjectAssignment.objects.filter(
            subject=obj
        ).select_related("teacher__user")
        return [
            {
                "id": a.teacher.id,
                "name": a.teacher.user.get_full_name(),
            }
            for a in assignments
        ]

    def get_student_count(self, obj):
        from students.models import Student
        class_ids = obj.class_assignments.values_list("school_class_id", flat=True)
        return Student.objects.filter(school_class_id__in=class_ids).distinct().count()
