from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.permissions import IsParent
from .models import Parent



class ParentDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def get(self, request):
        parent = Parent.objects.get(user=request.user)
        data = {
            "message": f"Welcome to the parent dashboard, {parent.user.username}!",
            "parent_id": parent.id,
            "children": [child.user.username for child in parent.children.all()],
        }
        return Response(data)