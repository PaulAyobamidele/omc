from rest_framework import serializers
from django.db.models import Sum
from .models import GradeEntry
from classes.models import Term


class GradeEntrySerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    max_score = serializers.IntegerField(read_only=True)
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.user.get_full_name", read_only=True)
    subject_name = serializers.CharField(source="class_subject.subject.name", read_only=True)
    class_name = serializers.CharField(source="class_subject.school_class.name", read_only=True)
    term_display = serializers.CharField(source="term.__str__", read_only=True)

    class Meta:
        model = GradeEntry
        fields = [
            "id", "student", "student_name",
            "class_subject", "subject_name", "class_name",
            "term", "term_display",
            "category", "category_display",
            "score", "max_score",
            "teacher", "teacher_name",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "teacher", "created_at", "updated_at",
            "category_display", "max_score",
            "student_name", "teacher_name", "subject_name",
            "class_name", "term_display",
        ]

    def validate_category(self, value):
        valid = [c[0] for c in GradeEntry.CATEGORY_CHOICES]
        if value not in valid:
            raise serializers.ValidationError(
                f"Invalid category. Must be one of: {', '.join(valid)}"
            )
        return value

    def validate_score(self, value):
        if value < 0:
            raise serializers.ValidationError("Score cannot be negative.")
        return value

    def validate(self, data):
        request = self.context["request"]
        teacher = getattr(request.user, "teacher_profile", None)

        if not teacher:
            raise serializers.ValidationError("Teacher profile not found.")

        student = data.get("student")
        class_subject = data.get("class_subject")
        category = data.get("category")
        score = data.get("score")

        if student and class_subject:
            if student.school_class != class_subject.school_class:
                raise serializers.ValidationError(
                    "This student is not in the class for this subject."
                )

        if category and score is not None:
            max_score = GradeEntry.CATEGORY_MAX_SCORES.get(category, 100)
            if score > max_score:
                raise serializers.ValidationError(
                    f"{category} max score is {max_score}. You entered {score}."
                )

        return data

    def create(self, validated_data):
        teacher = self.context["request"].user.teacher_profile
        validated_data["teacher"] = teacher

        if "term" not in validated_data or validated_data["term"] is None:
            active_term = Term.objects.filter(is_active=True).first()
            if not active_term:
                raise serializers.ValidationError({"term": "No active term. Please specify a term."})
            validated_data["term"] = active_term

        return super().create(validated_data)


class GradeEntryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeEntry
        fields = ["score"]

    def validate_score(self, value):
        if value < 0:
            raise serializers.ValidationError("Score cannot be negative.")
        max_score = GradeEntry.CATEGORY_MAX_SCORES.get(self.instance.category, 100)
        if value > max_score:
            raise serializers.ValidationError(
                f"{self.instance.category} max score is {max_score}."
            )
        return value


class StudentSubjectSummarySerializer(serializers.Serializer):
    subject_id = serializers.IntegerField()
    subject_name = serializers.CharField()
    grades = serializers.ListField()
    total_score = serializers.FloatField()
    total_max = serializers.FloatField()
    percentage = serializers.FloatField()
