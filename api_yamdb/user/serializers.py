from rest_framework import serializers
from .models import User


class UserSignupSerializer(serializers.Serializer):
    class Meta:
        fields = 'email', 'username'
        model = User


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
