from rest_framework import serializers
from .models import SchoolClass, ClassSubject
from teachers.models import Teacher
from subjects.models import Subject

class SchoolClassSerializer(serializers.ModelSerializer):
    class_teacher_name = serializers.CharField(
        source='class_teacher.user.get_full_name', read_only=True
    )

    class Meta:
        model = SchoolClass
        fields = ['id', 'name', 'class_teacher', 'class_teacher_name']

class ClassSubjectSerializer(serializers.ModelSerializer):
    school_class_name = serializers.CharField(source='school_class.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)

    class Meta:
        model = ClassSubject
        fields = ['id', 'school_class', 'school_class_name', 'subject', 'subject_name', 'teacher', 'teacher_name']
