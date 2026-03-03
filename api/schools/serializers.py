from rest_framework import serializers
from django.utils.text import slugify
from .models import School


class SchoolPublicSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = ['id', 'name', 'slug', 'logo_url', 'primary_color', 'address', 'phone', 'email']

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        return None


class SchoolUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['name', 'logo', 'primary_color', 'address', 'phone', 'email']


class SchoolRegisterSerializer(serializers.Serializer):
    # School fields
    school_name = serializers.CharField(max_length=200)
    slug = serializers.SlugField(max_length=100, required=False)
    primary_color = serializers.CharField(max_length=7, default='#2563eb', required=False)
    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    school_email = serializers.EmailField(required=False, allow_blank=True)

    # Admin user fields
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate_slug(self, value):
        if School.objects.filter(slug=value).exists():
            raise serializers.ValidationError('This URL is already taken. Choose a different one.')
        return value

    def validate(self, data):
        slug = data.get('slug') or slugify(data['school_name'])
        if not data.get('slug'):
            # Auto-generate and ensure uniqueness
            base = slug
            counter = 1
            while School.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
        data['slug'] = slug
        return data
