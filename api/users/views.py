from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import SignUpSerializer
from .models import User


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers import UserMeSerializer


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]
    
    
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)