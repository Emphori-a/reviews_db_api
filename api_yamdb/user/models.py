import re
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework.exceptions import ValidationError
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self,
                    role='',
                    username='',
                    bio='',
                    email='',
                    first_name='',
                    last_name='',
                    **extra_fields):
        if username == 'me':
            raise ValidationError('Недопустимое имя пользователя')
        if not re.match(r'^[\w.@+-]+\Z', str(username)):
            raise ValidationError(
                'Пользователь содержит недопустимые символлы')

        email = self.normalize_email(email)

        user = self.model(
            role=role,
            username=username,
            bio=bio,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.save(using=self.db)
        return user


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'


class User(AbstractUser):
    ROLE = [
        ('USER', 'User'),
        ('MODERATOR', 'Moderator'),
        ('ADMIN', 'Admin'),
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

    def is_admin(self):
        return (self.role == ADMIN
                or self.is_staff or self.is_superuser)

    def is_moderator(self):
        return (self.role == MODERATOR
                or self.is_staff or self.is_superuser)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
