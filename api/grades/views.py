from django.shortcuts import render
from rest_framework import generics
from .models import Grade
from .serializers import GradeSerializer
from .permissions import IsTeacher
from users.permissions import IsParent
from rest_framework.permissions import IsAuthenticated



class GradeCreateView(generics.CreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsTeacher]


class StudentGradesView(generics.ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role != 'student':
            return Grade.objects.none()
        student_profile = user.student_profile
        return Grade.objects.filter(student=student_profile)
    
    
class ParentGradesView(generics.ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsParent]
    
    
    def get_queryset(self):
        user = self.request.user
        if user.role != 'parent':
            return Grade.objects.none()
        parent_profile = user.parent_profile
        children = parent_profile.students.all()
        return Grade.objects.filter(student__in=children)