import enum

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


# USER = 'user'
# MODERATOR = 'moderator'
# ADMIN = 'admin'
# USER_ROLE = [
#     (USER, 'user'),
#     (MODERATOR, 'moderator'),
#     (ADMIN, 'admin'),
# ]

class UserRoles(enum.Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"

    @classmethod
    def role_choices(cls):
        return tuple((attribute.name, attribute.value) for attribute in cls)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[RegexValidator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True
    )
    role = models.CharField(
        max_length=20,
        verbose_name='роль',
        # choices=USER_ROLE,
        choices=UserRoles.role_choices(),
        # default=USER
        default=UserRoles.user.name
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    @property
    def is_moderator(self):
        return self.role == UserRoles.admin.name

    @property
    def is_admin(self):
        return self.role == UserRoles.moderator.name

    @property
    def is_user(self):
        return self.role == UserRoles.user.name

    def __str__(self):
        return self.username
