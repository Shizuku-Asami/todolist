from click import style
from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label="Email Address",
        help_text="Email address will be used for signing in.",
        max_length=254,
    )
    password = serializers.CharField(
        write_only=True,
        max_length=32,
        min_length=8,
        style={"input_type": "password"},
        help_text="Password must be at least 8 characters and cannot be longer than 32 characters.",
    )

    class Meta:
        model = User

    def create(self, data):
        print(data)
        return User.objects.create_user(**data)