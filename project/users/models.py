from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name='username')
    email = models.EmailField(unique=True, verbose_name='email address')
    name = models.CharField(max_length=150, blank=True, null=True, verbose_name='name')
    surname = models.CharField(max_length=150, blank=True, null=True, verbose_name='surname')
    birth_date = models.DateTimeField(blank=True, null=True, verbose_name='birth_date')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'email'
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
