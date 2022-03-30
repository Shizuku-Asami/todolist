from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.response import Response

from .models import User
from .serializers import LoginSerializer ,RegistrationSerializer


class UserCreateAPIView(views.APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        payload = request.data
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(data=user_data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        payload = request.data
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)