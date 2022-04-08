from django.db import models

from users.models import User


class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist_user")
    name = models.CharField(help_text="The todolist name.", max_length=254)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
