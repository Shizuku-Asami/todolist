from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import TodoListSerializer
from .models import TodoList
from .permissions import IsOwner


class TodoListViewSet(viewsets.ModelViewSet):
    serializer_class = TodoListSerializer
    queryset = TodoList.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id)