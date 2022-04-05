from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name='username')
    email = models.EmailField(unique=True, verbose_name='email address')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'email'
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
