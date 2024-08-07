from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    avatar = models.ImageField(upload_to='users/avatars', verbose_name='avatar', **NULLABLE)
    phone = models.CharField(max_length=10, verbose_name='phone number', **NULLABLE, help_text='Введите номер телефона')
    country = models.CharField(max_length=50, verbose_name='country', help_text='Введите страну', **NULLABLE)

    token = models.CharField(max_length=100, verbose_name='token', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email
