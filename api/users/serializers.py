from rest_framework import serializers
from .models import User
from teachers.models import Teacher
from students.models import Student
from parents.models import Parent




class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        role = validated_data.pop('role')
        if role == "student":
            raise serializers.ValidationError("Students cannot sign up themselves. Only parents can add students.")

        password = validated_data.pop('password')
        user = User(**validated_data, role=role)
        user.set_password(password)
        user.save()

        if role == "parent":
            Parent.objects.create(user=user)
        elif role == "teacher":
            Teacher.objects.create(user=user)

        return user

    
    
class UserMeSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'first_name', 'last_name', 'email', 'profile']

    def get_profile(self, obj):
        if obj.role == "teacher":
            try:
                teacher_profile = Teacher.objects.get(user=obj)
                return {
                    "subjects": [subject.name for subject in teacher_profile.subjects.all()],
                    "years_of_experience": teacher_profile.years_of_experience
                }
            except Teacher.DoesNotExist:
                return None
        elif obj.role == "student":
            try:
                student_profile = Student.objects.get(user=obj)
                parent = student_profile.parent
                return {
                    "parent": {
                        "id": parent.id,
                        "name": f"{parent.user.first_name} {parent.user.last_name}"
                    }
                }
            except Student.DoesNotExist:
                return None
        elif obj.role == "parent":
            try:
                parent_profile = Parent.objects.get(user=obj)
                return {
                    "children": [
                        {
                            "id": child.id,
                            "name": f"{child.user.first_name} {child.user.last_name}"
                        } for child in parent_profile.students.all()
                    ]
                }
            except Parent.DoesNotExist:
                return None
        return None
