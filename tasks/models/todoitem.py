from django.db import models

from .todolist import TodoList


class TodoItem(models.Model):
    todolist = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="todoitem_todolist")
    name = models.CharField(max_length=254)
    description = models.TextField(default="")
    is_done = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}|{self.todolist}"
