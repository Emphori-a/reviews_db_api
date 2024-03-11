import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CheckUserSerializer:
    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя.'
            )
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError(
                ('Имя пользователя может содержать только буквы, '
                 'цифры и знаки @ / . / + / - / _')
            )
        return username


class UserSignupSerializer(serializers.Serializer, CheckUserSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }
