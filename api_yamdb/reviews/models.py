from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import IntegrityError, models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
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
        return self.role == self.ADMIN


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
        verbose_name='Название',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None,
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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        max_length=256,
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

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        existing_reviews = Review.objects.filter(title=self.title,
                                                 author=self.author)
        if self.pk is None and existing_reviews.exists():
            raise IntegrityError('Отзыв от данного автора для данного'
                                 'произведения уже существует.')
        super().save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        max_length=256,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления комментария',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('id',)

    def __str__(self):
        return self.text
