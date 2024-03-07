from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from user.models import User


class PublishedModel(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

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
        max_length=256,
        help_text='Название произведения, не более 256 символов'
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[MaxValueValidator(timezone.now().year)],
        help_text='Год выпуска произведения (не может быть больше текущего).'
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
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Минимальная оценка - 1, максимальная оценка - 10'
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
        # unique=True
    )

    # не уверена, что это нужно, но все же
    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']


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
        null=True,
        related_name='comments'
    )
