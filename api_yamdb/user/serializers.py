import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model

User = get_user_model()


class RegexValidator:
    pass


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150
    )
    email = serializers.EmailField(max_length=254)

    def validate_username(self, username):
        if username == 'me' or not re.match(r'^[\w.@+-]+\Z', username):
            raise ValidationError('Пользователь не соттветствует стандарту')
        existing_user = User.objects.filter(username=username)
        if existing_user.exists():
            raise serializers.ValidationError('Пользователь с таким именем уже зарегистрирован!')

        return username

    def validate_email(self, email):
        existing_email = User.objects.filter(email=email)
        if existing_email.exists():
            raise serializers.ValidationError('Пользователь с таким Email уже зарегистрирован!')
        return email

class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.EmailField(max_length=150)
    confirmation_code = serializers.CharField()



class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)




