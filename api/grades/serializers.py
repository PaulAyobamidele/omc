from rest_framework import serializers
from .models import Grade
from teachers.models import Teacher

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'student', 'teacher', 'subject', 'score', 'comments', 'created_at']
        read_only_fields = ['teacher', 'created_at']

    def create(self, validated_data):
        teacher_profile = Teacher.objects.get(user=self.context['request'].user)
        validated_data['teacher'] = teacher_profile
        return super().create(validated_data)
