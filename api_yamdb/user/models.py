from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.constants import (
    MAX_EMAIL_LENGTH, MAX_ROLE_LENGHT, MAX_USERNAME_LENGHT
)


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
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
    )
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=MAX_USERNAME_LENGHT,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')],
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
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

        username_validator = UnicodeUsernameValidator()
        try:
            username_validator(self.username)
        except ValidationError as e:
            raise ValidationError({'username': e.messages})

        if self.username.lower() == 'me':
            raise ValidationError({'username': ['Нельзя использовать "me" в '
                                                'качестве имени '
                                                'пользователя.']})

        if User.objects.filter(username=self.username).exclude(
            pk=self.pk
        ).exists():
            raise ValidationError(
                {'username': ['Имя пользователя уже занято']}
            )

        # Проверка на уникальность email
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': [f'Email {self.email} уже занят']})

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
