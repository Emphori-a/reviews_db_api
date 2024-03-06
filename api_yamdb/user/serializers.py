from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegexValidator:
    pass


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150
    )
    email = serializers.EmailField(max_length=254)




class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    confirmation_code = serializers.CharField()


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150
    )
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    pass
