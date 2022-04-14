import json
import re

from django.http import QueryDict
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import TodoListSerializer, TodoItemSerializer
from .models import TodoList
from .permissions import IsOwner


class TodoListViewSet(viewsets.ModelViewSet):
    serializer_class = TodoListSerializer
    queryset = TodoList.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        todoitems = []
        self.perform_create(serializer)
        # This portion of code should be refactored
        ### BEGIN ###
        if "todoitem_todolist" in data.keys():
            for element in dict(data)["todoitem_todolist"]:
                element = element.replace("'", '"')
                if '"is_done": False' in element:
                    element = element.replace('"is_done": False', '"is_done": false')
                if '"is_done": True' in element:
                    element = element.replace('"is_done": True', '"is_done": true')
                element = json.loads(element)
                element["todolist"] = serializer.data["id"]
                query_element = QueryDict('', mutable=True)
                query_element.update(element)
                todoitem_serializer = TodoItemSerializer(data=query_element)
                todoitem_serializer.is_valid(raise_exception=True)
                todoitem_serializer.save()
                todoitems.append(todoitem_serializer.data)
        response_data = serializer.data.copy()
        response_data["todoitem_todolist"] = todoitems
        ### END ###
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id)
