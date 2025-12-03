from rest_framework import serializers
from .models import GradeEntry
from teachers.models import Teacher
from students.models import Student
from django.db.models import Sum

class GradeEntrySerializer(serializers.ModelSerializer):
    # Readable category name for UI
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    # Total score for this student in this subject (read-only)
    total_score = serializers.SerializerMethodField(read_only=True)

    
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    class_subject_name = serializers.CharField(source='class_subject.subject.name', read_only=True)
    
    
    
    class Meta:
        model = GradeEntry
        fields = [
            'id',
            'student',
            'student_name',
            'class_subject',
            'class_subject_name',
            'category',
            'category_display',
            'score',
            'teacher',
            'teacher_name',
            'created_at',
            'total_score',
        ]
        read_only_fields = ['id', 'teacher', 'created_at', 'category_display', 'total_score', 'student_name', 'teacher_name', 'class_subject_name']

    def validate_category(self, value):
        valid_categories = [choice[0] for choice in GradeEntry.CATEGORY_CHOICES]
        if value not in valid_categories:
            raise serializers.ValidationError(
                f"Invalid category. Must be one of: {', '.join(valid_categories)}"
            )
        return value

    def validate(self, data):
        request = self.context['request']
        teacher_profile = getattr(request.user, 'teacher_profile', None)

        if not teacher_profile:
            raise serializers.ValidationError("Teacher profile not found for the current user.")

        student = data.get('student')
        class_subject = data.get('class_subject')

        # Check teacher assigned to this subject/class
        if class_subject.teacher and class_subject.teacher != teacher_profile:
            raise serializers.ValidationError("You are not assigned to teach this subject/class.")

        # Check teacher has class access for this student
        if student.school_class != class_subject.school_class:
            raise serializers.ValidationError("You cannot grade this student because they are not in this class.")

        return data

    def create(self, validated_data):
        teacher_profile = getattr(self.context['request'].user, 'teacher_profile', None)
        validated_data['teacher'] = teacher_profile
        return super().create(validated_data)

    def get_total_score(self, obj):
        """
        Returns the cumulative score for this student in this subject (class_subject).
        """
        total = GradeEntry.objects.filter(
            student=obj.student,
            class_subject=obj.class_subject
        ).aggregate(total=Sum('score'))['total'] or 0
        return float(total)

class SubjectSummarySerializer(serializers.Serializer):
    subject_id = serializers.IntegerField()
    subject_name = serializers.CharField()
    total_score = serializers.DecimalField(max_digits=6, decimal_places=2)
    average_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)

class StudentSummarySerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    subjects = SubjectSummarySerializer(many=True)
    overall_total = serializers.DecimalField(max_digits=6, decimal_places=2)
    overall_average = serializers.DecimalField(max_digits=5, decimal_places=2)
    overall_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)


