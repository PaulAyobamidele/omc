# reports/serializers.py

from rest_framework import serializers

class GradeItemSerializer(serializers.Serializer):
    category = serializers.CharField()
    score = serializers.FloatField()
    maximum = serializers.FloatField()
    percentage = serializers.FloatField()

class SubjectReportSerializer(serializers.Serializer):
    subject_id = serializers.IntegerField()
    subject_name = serializers.CharField()
    teacher_name = serializers.CharField(allow_null=True)
    grades = GradeItemSerializer(many=True)
    total_score = serializers.FloatField()
    total_maximum = serializers.FloatField()
    average_percentage = serializers.FloatField()

class StudentReportSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    class_name = serializers.CharField()
    term = serializers.CharField()
    session = serializers.CharField()
    subjects = SubjectReportSerializer(many=True)
    overall_average = serializers.FloatField()
