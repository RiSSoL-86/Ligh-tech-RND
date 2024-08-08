from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    USERNAME_FIELD = 'email'
    username = models.CharField(
        unique=True,
        max_length=50,
        validators=[UnicodeUsernameValidator(), ],
        verbose_name='Никнейм пользователя',
        help_text='Укажите никнейм пользователя'
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя пользователя',
        help_text='Укажите имя пользователя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия пользователя',
        help_text='Укажите фамилию пользователя'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='E-mail пользователя',
        help_text='Укажите e-mail пользователя'
    )
    created_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации',
        help_text='Дата регистрации пользователя'
    )
    updated_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменений',
        help_text='Дата изменений данных пользователя'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
