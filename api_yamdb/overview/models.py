from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
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
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


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
