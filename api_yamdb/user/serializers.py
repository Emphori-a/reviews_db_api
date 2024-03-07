import re

from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class RegexValidator:
    pass


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=254)
    confirmation_code = serializers.CharField()


class UserProfileSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = '__all__'
