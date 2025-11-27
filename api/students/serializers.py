# students/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from students.models import Student
from parents.models import Parent
import random, string

User = get_user_model()


def generate_username(first_name, last_name):
    suffix = ''.join(random.choices(string.digits, k=4))
    return f"{first_name.lower()}.{last_name.lower()}_{suffix}"


def generate_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class UnifiedStudentSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(required=False)
    class_level = serializers.CharField()  # maps to student_class
    parent_id = serializers.IntegerField(required=False)

    # Returned fields
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
    student_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        request_user = self.context['request'].user

        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        class_level = validated_data.pop('class_level')
        date_of_birth = validated_data.pop('date_of_birth', None)
        parent_id = validated_data.pop('parent_id', None)

        # Determine parent
        parent_profile = None

        # If parent is creating:
        if hasattr(request_user, "parent_profile"):
            parent_profile = request_user.parent_profile

        # If teacher: must supply parent_id
        elif request_user.role == "teacher":
            if not parent_id:
                raise serializers.ValidationError({
                    "parent_id": ["Teacher must provide parent_id."]
                })
            parent_profile = Parent.objects.filter(id=parent_id).first()
            if not parent_profile:
                raise serializers.ValidationError({
                    "parent_id": ["Parent with this ID does not exist."]
                })

        # If admin: parent_id optional
        elif request_user.role == "admin":
            if parent_id:
                parent_profile = Parent.objects.filter(id=parent_id).first()

        # Create system user
        username = generate_username(first_name, last_name)
        password = generate_password()

        student_user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role="student"
        )

        # Create student profile
        student_profile = Student.objects.create(
            user=student_user,
            parent=parent_profile,
            class_level=class_level,  # matches DB model
            date_of_birth=date_of_birth,
        )

        return {
            "student_id": student_profile.id,
            "username": username,
            "password": password,
            "class_level": class_level
        }
