from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator

from api_yamdb.constants import MAX_ROLE_LENGHT, MAX_USERNAME_LENGHT


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name=('Имя пользователя'),
        max_length=MAX_USERNAME_LENGHT,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': ('Пользователь с таким именем уже существует.'),
        },
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=MAX_ROLE_LENGHT,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        if username == 'me':
            raise ValidationError(
                'Использование имени "me" запрещено'
            )
        raise self.cleaned_data

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
