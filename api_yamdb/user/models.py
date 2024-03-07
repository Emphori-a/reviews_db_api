import re
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework.exceptions import ValidationError
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, **extra_fields):
        if username == 'me':
            raise ValidationError('Недопустимое имя пользователя')
        if not re.match(r'^[\w.@+-]+\Z', str(username)):
            raise ValidationError(
                'Пользователь содержит недопустимые символлы')
        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.save(using=self.db)
        return user


class User(AbstractUser):
    ROLE = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        choices=ROLE,
        default='user',
        max_length=25,
        blank=True
    )
    username = models.CharField('username', max_length=150, unique=True)
    bio = models.TextField(blank=True)
    email = models.EmailField('email', max_length=254, unique=True)
    first_name = models.CharField('name', max_length=150, blank=True)
    last_name = models.CharField('surname', max_length=150, blank=True)

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
