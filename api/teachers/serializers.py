from rest_framework import serializers
from .models import Teacher, TeacherSubjectAssignment


class TeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            "id", "full_name", "username", "email",
            "years_of_experience", "subjects",
        ]

    def get_subjects(self, obj):
        assignments = obj.subject_assignments.select_related("subject").all()
        return [
            {"id": a.subject.id, "name": a.subject.name}
            for a in assignments
        ]


class TeacherSubjectAssignmentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.user.get_full_name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = TeacherSubjectAssignment
        fields = ["id", "teacher", "teacher_name", "subject", "subject_name", "assigned_at"]
        read_only_fields = ["assigned_at"]
