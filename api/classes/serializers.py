from rest_framework import serializers
from .models import SchoolClass, ClassSubject, AcademicSession, Term


class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ["id", "name", "start_date", "end_date", "is_active"]


class TermSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source="session.name", read_only=True)
    display_name = serializers.CharField(source="get_name_display", read_only=True)

    class Meta:
        model = Term
        fields = ["id", "session", "session_name", "name", "display_name", "start_date", "end_date", "is_active"]


class SchoolClassSerializer(serializers.ModelSerializer):
    class_teacher_name = serializers.CharField(
        source="class_teacher.user.get_full_name", read_only=True
    )
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = SchoolClass
        fields = ["id", "name", "class_teacher", "class_teacher_name", "student_count"]

    def get_student_count(self, obj):
        return obj.students.count()


class ClassSubjectSerializer(serializers.ModelSerializer):
    school_class_name = serializers.CharField(source="school_class.name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.user.get_full_name", read_only=True)

    class Meta:
        model = ClassSubject
        fields = [
            "id", "school_class", "school_class_name",
            "subject", "subject_name",
            "teacher", "teacher_name",
        ]
