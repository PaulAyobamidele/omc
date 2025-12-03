from rest_framework import serializers
from teachers.models import Subject, Teacher, TeacherSubjectAssignment
from students.models import Student
from django.contrib.auth import get_user_model

User = get_user_model()

class SubjectSerializer(serializers.ModelSerializer):
    """
    Serialize Subject info.
    """
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description']


class SubjectDetailSerializer(serializers.ModelSerializer):
    """
    Include teacher assignments and students per subject.
    """
    teachers = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'teachers', 'students']

    def get_teachers(self, obj):
        assignments = TeacherSubjectAssignment.objects.filter(subject=obj)
        return [
            {
                'id': t.teacher.id,
                'name': f"{t.teacher.user.first_name} {t.teacher.user.last_name}"
            } for t in assignments
        ]

    def get_students(self, obj):
        classes = obj.class_subjects.all()
        students = []
        for cs in classes:
            students += list(cs.school_class.students.all())
        # Remove duplicates
        unique_students = {s.id: s for s in students}.values()
        return [
            {
                'id': s.id,
                'name': f"{s.user.first_name} {s.user.last_name}"
            } for s in unique_students
        ]
