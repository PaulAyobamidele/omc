from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import School
from .serializers import SchoolPublicSerializer, SchoolUpdateSerializer, SchoolRegisterSerializer
from users.permissions import IsAdmin


class SchoolPublicView(APIView):
    """Public endpoint — returns school branding. No auth required."""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            school = School.objects.get(slug=slug, is_active=True)
        except School.DoesNotExist:
            return Response({'detail': 'School not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(SchoolPublicSerializer(school, context={'request': request}).data)


class SchoolDetailView(generics.RetrieveUpdateAPIView):
    """School admin can view and update their school settings."""
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = SchoolUpdateSerializer

    def get_object(self):
        return self.request.school


class SchoolRegisterView(APIView):
    """Self-service school registration. Creates school + first admin user."""
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = SchoolRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        from django.contrib.auth import get_user_model
        from parents.models import Parent
        from teachers.models import Teacher

        User = get_user_model()

        if User.objects.filter(username=data['username']).exists():
            return Response(
                {'username': ['This username is already taken.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        school = School.objects.create(
            name=data['school_name'],
            slug=data['slug'],
            primary_color=data.get('primary_color', '#2563eb'),
            address=data.get('address', ''),
            phone=data.get('phone', ''),
            email=data.get('school_email', ''),
        )

        user = User(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data.get('email', ''),
            role='admin',
            school=school,
            is_staff=True,
        )
        user.set_password(data['password'])
        user.save()

        return Response({
            'school': SchoolPublicSerializer(school, context={'request': request}).data,
            'detail': f'School "{school.name}" registered. You can now log in at /{school.slug}/login',
        }, status=status.HTTP_201_CREATED)
