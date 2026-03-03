from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from users.permissions import IsParent, IsAdminOrTeacher
from .models import Parent
from .serializers import ParentSerializer


class ParentDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def get(self, request):
        parent = request.user.parent_profile
        serializer = ParentSerializer(parent)
        return Response(serializer.data)


class ParentListView(generics.ListAPIView):
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def get_queryset(self):
        qs = Parent.objects.select_related("user").prefetch_related(
            "students__user", "students__school_class"
        ).filter(school=self.request.school)
        search = self.request.query_params.get("search")
        if search:
            qs = (
                qs.filter(user__username__icontains=search)
                | qs.filter(user__first_name__icontains=search)
                | qs.filter(user__last_name__icontains=search)
            )
        return qs
