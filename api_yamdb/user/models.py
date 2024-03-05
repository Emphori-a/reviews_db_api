from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class User(AbstractUser):
    CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(max_length=254, validators=[validators.validate_email])
    role = models.CharField(blank=True, choices=CHOICES, default='user', max_length=20)
    bio = models.TextField(blank=True)
    first_name = models.CharField(blank=True, max_length=150)
    last_name = models.CharField(blank=True, max_length=150)
