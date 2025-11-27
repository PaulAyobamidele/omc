# students/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UnifiedStudentSerializer
from users.permissions import IsTeacher, IsParent

class CreateStudentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Only allow teachers or parents
        if not (request.user.is_teacher() or request.user.is_parent()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UnifiedStudentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)
