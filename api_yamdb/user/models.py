from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import (MAX_LENGTH_ROLE, MAX_LENGTH_USER)


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'


class User(AbstractUser):
    ROLE = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE,
        default=USER,
        max_length=MAX_LENGTH_ROLE,
        blank=True
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=MAX_LENGTH_USER,
        unique=True
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LENGTH_USER,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LENGTH_USER,
        blank=True
    )

    def is_admin(self):
        return (self.role == ADMIN
                or self.is_staff or self.is_superuser)

    def is_moderator(self):
        return (self.role == MODERATOR
                or self.is_staff or self.is_superuser)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
