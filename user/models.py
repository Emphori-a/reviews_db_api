from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(max_length=254)
    role = models.CharField(choices=CHOICES, default='user')
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
