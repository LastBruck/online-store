from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Avatar


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "username", "password"


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = "src", "alt"


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(many=False, required=False)

    class Meta:
        model = Profile
        fields = "__all__"
