from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year
from api_yamdb.constants import MAX_NAME_LENGTH, MAX_LENGHT


User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        verbose_name="Категория",
        max_length=MAX_NAME_LENGTH
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_LENGHT] + (
            '...' if len(self.name) > MAX_LENGHT else ''
        )


class Genre(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=MAX_NAME_LENGTH
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_LENGHT] + (
            '...' if len(self.name) > MAX_LENGHT else ''
        )


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_NAME_LENGTH,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year]
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_LENGHT] + (
            '...' if len(self.name) > MAX_LENGHT else ''
        )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        max_length=MAX_NAME_LENGTH,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        validators=[MinValueValidator(1, message='Минимальная оценка - 1'),
                    MaxValueValidator(10, message='Максимальня оценка - 10')]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления отзыва',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text[:MAX_LENGHT] + (
            '...' if len(self.text) > MAX_LENGHT else ''
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        max_length=MAX_NAME_LENGTH,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления комментария',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:MAX_LENGHT] + (
            '...' if len(self.text) > MAX_LENGHT else ''
        )
