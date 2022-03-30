from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .utils import get_tokens_for_user


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
        return User.objects.create_user(**data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label="Email Address",
        max_length=254,
    )
    password = serializers.CharField(
        write_only=True,
        max_length=32,
        min_length=8,
        style={"input_type": "password"},
    )
    tokens = serializers.SerializerMethodField()


    class Meta:
        model = User

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])
        tokens = get_tokens_for_user(user)
        return tokens

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again.")
        tokens = self.get_tokens(attrs)
        return {"email": email, "tokens": tokens}
