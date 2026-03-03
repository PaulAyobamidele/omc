from rest_framework import serializers
from .models import Parent


class ParentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Parent
        fields = ["id", "full_name", "username", "email", "phone", "children"]

    def get_children(self, obj):
        return [
            {
                "id": child.id,
                "name": child.user.get_full_name(),
                "class": child.school_class.name if child.school_class else None,
            }
            for child in obj.students.select_related("user", "school_class").all()
        ]