from django.db import models


class Category(models.Model):
    name = models.CharField(
        verbose_name="Категория",
        max_length=256
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=256
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name="Год выпуска",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    rating = models.IntegerField(
        verbose_name="Рейтинг",
        null=True,
        default=None,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'
