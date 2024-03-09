from django.contrib.auth.models import AbstractUser
from django.db import models

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
    first_name = models.CharField('first_name', max_length=150, blank=True)
    last_name = models.CharField('last_name', max_length=150, blank=True)

    def is_admin(self):
        return (self.role == ADMIN
                or self.is_staff or self.is_superuser)

    def is_moderator(self):
        return (self.role == MODERATOR
                or self.is_staff or self.is_superuser)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
