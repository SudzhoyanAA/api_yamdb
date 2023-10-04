from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, IntegrityError


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        unique=True
    )

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
    )

    role = models.CharField(
<<<<<<< Updated upstream
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )

    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
=======
        max_length=20,
        verbose_name='роль',
        choices=USER_ROLE,
        default='user'
>>>>>>> Stashed changes
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        # return self.role == self.ADMIN
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
