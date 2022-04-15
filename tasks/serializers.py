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
    todoitem_todolist = TodoItemSerializer(many=True, required=False)

    class Meta:
        model = TodoList
        fields = "__all__"

    def create(self, validated_data):
        data = validated_data.copy()
        if "todoitem_todolist" in data.keys():
            todoitem_todolist_data = data.pop("todoitem_todolist")
        todolist = TodoList.objects.create(**data)
        data["id"] = todolist.id
        data["user"] = validated_data["user"]
        if "todoitem_todolist" in data.keys():
            for todoitem_data in todoitem_todolist_data:
                todoitem_data["todolist"] = todolist
                TodoItem.objects.create(**todoitem_data)
            todoitems = TodoItem.objects.filter(todolist=data["id"])
            todolist.todoitem_todolist.set(todoitems)
        return todolist

    def update(self, validated_data):
        # TODO: FIX UPDATE METHOD
        todoitem_todolist_data = validated_data.pop("todoitem_todolist")
        todolist = TodoList.objects.get(id=validated_data["id"])
        for key, value in validated_data:
            setattr(todolist, key, value)
        todoitems = TodoItem.objects.filter(todolist=validated_data["id"])
        for todoitem, todoitem_data in zip(todoitems, todoitem_todolist_data):
            for key, value in todoitem_data:
                setattr(todoitem, key, value)
                todoitem.save()
        todolist.save()
        return todolist
