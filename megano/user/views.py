from rest_framework import status
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSerializer
from django.contrib.auth.views import LogoutView
from .models import Profile, Avatar
import json


class SignUpView(APIView):
    def post(self, request: Request):
        data = json.loads(list(request.data.keys())[0])
        serializer = UserSerializer(data=data)
        username = data.get("username")

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            name = data.get("name")
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            try:
                user = User.objects.create_user(username=username, password=password)
                user.first_name = name
                user.save()
                Profile.objects.create(user=user, fullName=name)
                user = authenticate(username=username, password=password)
                login(request, user)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {"success": "Registered successfully"}, status=status.HTTP_201_CREATED
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(LogoutView):
    next_page = reverse_lazy("user:sign-in")


class SignInView(APIView):
    def post(self, request):
        data = json.loads(list(request.data.keys())[0])
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)

        return Response("Authentication successful", status=status.HTTP_200_OK)


class ProfileDetail(APIView):
    def get(self, request: Request):
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)
        serialized = ProfileSerializer(profile, many=False)
        return Response(serialized.data)

    def post(self, request: Request):
        data = request.data
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)

        profile.fullName = data.get("fullName")
        profile.phone = data.get("phone")
        profile.email = data.get("email")
        profile.save()

        return Response("Update successful", status=status.HTTP_200_OK)


class AvatarUpdateView(APIView):
    def post(self, request: Request):
        new_avatar = request.data.get("avatar")
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)
        avatar, created = Avatar.objects.get_or_create(profile_id=profile.pk)
        if str(new_avatar).endswith((".png", ".jpg", ".jpeg")):
            avatar.image = new_avatar
            avatar.save()
        else:
            return Response("Wrong file format", status=status.HTTP_400_BAD_REQUEST)
        return Response("Update successful", status=status.HTTP_200_OK)


class PasswordUpdateView(APIView):
    def post(self, request):
        user = request.user
        password_current = request.data.get("currentPassword")
        password = request.data.get("newPassword")

        if not user.check_password(password_current):
            return Response(
                {"error": "Неверный текущий пароль"}, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(password)
        user.save()

        return Response(
            {"success": "Пароль успешно обновлен"}, status=status.HTTP_200_OK
        )
