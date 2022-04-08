from rest_framework import serializers

from tasks.models import todolist

from .models import TodoList, TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = [
            "todolist",
            "name",
            "description",
            "is_done",
            "due_date",
            "created_at",
            "updated_at",
        ]


class TodoListSerializer(serializers.ModelSerializer):
    todoitem_todolist = TodoItemSerializer(many=True)

    class Meta:
        model = TodoList
        fields = "__all__"
