from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student
from parents.models import Parent
from classes.models import SchoolClass
import random
import string

User = get_user_model()


def generate_username(first_name, last_name):
    suffix = "".join(random.choices(string.digits, k=4))
    return f"{first_name.lower()}.{last_name.lower()}_{suffix}"


def generate_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$"
    return "".join(random.choices(chars, k=length))


class StudentListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    class_name = serializers.CharField(source="school_class.name", read_only=True)
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ["id", "full_name", "username", "class_name", "parent_name", "date_of_birth"]

    def get_parent_name(self, obj):
        if obj.parent:
            return obj.parent.user.get_full_name()
        return None


class CreateStudentSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    date_of_birth = serializers.DateField(required=False)
    school_class_id = serializers.IntegerField()
    parent_id = serializers.IntegerField(required=False)

    username = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
    student_id = serializers.IntegerField(read_only=True)

    def validate_school_class_id(self, value):
        request = self.context["request"]
        school = getattr(request, "school", None)
        qs = SchoolClass.objects.filter(id=value)
        if school:
            qs = qs.filter(school=school)
        if not qs.exists():
            raise serializers.ValidationError("School class not found.")
        return value

    def create(self, validated_data):
        request_user = self.context["request"].user
        school = getattr(self.context["request"], "school", None)

        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        school_class_id = validated_data["school_class_id"]
        date_of_birth = validated_data.get("date_of_birth")
        parent_id = validated_data.get("parent_id")

        parent_profile = None

        if request_user.role == "parent":
            parent_profile = request_user.parent_profile

        elif request_user.role == "teacher":
            if not parent_id:
                raise serializers.ValidationError({"parent_id": "Teacher must provide parent_id."})
            parent_profile = Parent.objects.filter(id=parent_id).first()
            if not parent_profile:
                raise serializers.ValidationError({"parent_id": "Parent not found."})

        elif request_user.role == "admin":
            if parent_id:
                parent_profile = Parent.objects.filter(id=parent_id).first()

        school_class = SchoolClass.objects.get(id=school_class_id)

        username = generate_username(first_name, last_name)
        password = generate_password()

        student_user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role="student",
            school=school,
        )

        student = Student.objects.create(
            user=student_user,
            parent=parent_profile,
            school_class=school_class,
            date_of_birth=date_of_birth,
        )

        return {
            "student_id": student.id,
            "username": username,
            "password": password,
            "school_class": school_class.name,
            "first_name": first_name,
            "last_name": last_name,
        }
