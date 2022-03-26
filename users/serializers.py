from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="Email address will be used for signing in.",
        max_length="254",
        verbose_name="email address",
    )
    password = serializers.CharField(
        write_only=True,
        max_length=32,
        min_length=8,
        help_text="Password must be at least 8 characters and cannot be longer than 32 characters.",
    )

    class Meta:
        model = User
