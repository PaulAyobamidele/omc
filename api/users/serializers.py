from rest_framework import serializers
from .models import User
from teachers.models import Teacher, TeacherSubjectAssignment
from students.models import Student
from parents.models import Parent


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "password", "role", "first_name", "last_name", "email"]

    def validate_role(self, value):
        if value == "student":
            raise serializers.ValidationError(
                "Students cannot sign up directly. A parent or admin must create student accounts."
            )
        if value == "admin":
            raise serializers.ValidationError(
                "Admin accounts must be created by an existing admin."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        school = validated_data.pop("school", None)
        user = User(**validated_data)
        user.school = school
        user.set_password(password)
        user.save()

        if user.role == "parent":
            Parent.objects.create(user=user, school=school)
        elif user.role == "teacher":
            Teacher.objects.create(user=user)

        return user


class UserMeSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "role", "first_name", "last_name", "email", "profile"]

    def get_profile(self, obj):
        if obj.role == "teacher":
            teacher = getattr(obj, "teacher_profile", None)
            if not teacher:
                return None
            assignments = TeacherSubjectAssignment.objects.filter(
                teacher=teacher
            ).select_related("subject")
            return {
                "teacher_id": teacher.id,
                "years_of_experience": teacher.years_of_experience,
                "subjects": [
                    {"id": a.subject.id, "name": a.subject.name}
                    for a in assignments
                ],
            }

        elif obj.role == "student":
            student = getattr(obj, "student_profile", None)
            if not student:
                return None
            result = {
                "student_id": student.id,
                "school_class": None,
                "parent": None,
            }
            if student.school_class:
                result["school_class"] = {
                    "id": student.school_class.id,
                    "name": student.school_class.name,
                }
            if student.parent:
                result["parent"] = {
                    "id": student.parent.id,
                    "name": student.parent.user.get_full_name(),
                }
            return result

        elif obj.role == "parent":
            parent = getattr(obj, "parent_profile", None)
            if not parent:
                return None
            return {
                "parent_id": parent.id,
                "phone": parent.phone,
                "children": [
                    {
                        "id": child.id,
                        "name": child.user.get_full_name(),
                        "class": child.school_class.name if child.school_class else None,
                    }
                    for child in parent.students.select_related("user", "school_class").all()
                ],
            }

        return None

