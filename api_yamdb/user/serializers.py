import re

from rest_framework import serializers

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate(self, data):
        existing_user_by_username = User.objects.filter(
            username=data['username']).first()
        existing_user_by_email = User.objects.filter(
            email=data['email']).first()

        if existing_user_by_username != existing_user_by_email:
            error_msg = {}
            if existing_user_by_username:
                error_msg[
                    'username'] = ('Пользователь с таким '
                                   'username уже существует.')
            if existing_user_by_email:
                error_msg['email'] = ('Пользователь с таким '
                                      'email уже существует.')
            raise serializers.ValidationError(error_msg)

        return data

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email'])
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            f'Код подтверждения для пользователя {user.username}',
            f'Ваш Код подтверждения для пользователя {user.username}: '
            f'{confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )
        return user


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        if not data.get('username'):
            raise serializers.ValidationError("Нет данных в запросе!")

        user = get_object_or_404(User, username=data.get('username'))
        if user:
            raise serializers.ValidationError('Пользователь не найден')

        if not default_token_generator.check_token(
                user,
                data.get['confirmation_code']
        ):
            raise serializers.ValidationError('Неверный код подтверждения')

        return {'token': str(AccessToken.for_user(user))}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }
