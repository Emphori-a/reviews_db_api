from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from api_yamdb.settings import (MAX_LENGTH_NAME, MAX_LENGTH_SLUG, MIN_SCORE,
                                MAX_SCORE, LEN_TEXT_TO_REPRESENT)
from user.models import User
from .validators import validate_year


class PublishedModel(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=MAX_LENGTH_NAME)
    slug = models.SlugField(unique=True, max_length=MAX_LENGTH_SLUG)

    def __str__(self):
        return self.slug

    class Meta:
        abstract = True


class Category(PublishedModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['slug']


class Genre(PublishedModel):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['slug']


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_NAME,
        help_text=f'Название произведения, не более {MAX_LENGTH_NAME} символов'
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year],
        help_text='Год выпуска произведения не может быть больше текущего.'
    )
    description = models.TextField(verbose_name='Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        blank=True,
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        blank=True,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['year']

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Оценка',
        validators=[MinValueValidator(MIN_SCORE),
                    MaxValueValidator(MAX_SCORE)],
        help_text=(f'Минимальная оценка - {MIN_SCORE}, '
                   f'максимальная оценка - {MAX_SCORE}')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время отзыва',
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:LEN_TEXT_TO_REPRESENT]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время комментария',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:LEN_TEXT_TO_REPRESENT]
