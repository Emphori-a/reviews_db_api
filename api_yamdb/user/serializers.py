import re
from abc import ABC

from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

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


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=254)
    confirmation_code = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

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
