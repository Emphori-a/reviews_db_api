from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from user.models import User


# создала пока здесь после создания приложения user добавить импорт, убрать
# класс, не забыть поменять в settings AUTH_USER_MODEL(зарегать в админке?)
#class User(AbstractUser):
#    pass


class PublishedModel(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    # возможно стоит поменять на слаг?
    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(PublishedModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(PublishedModel):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    # подумать над годом
    year = models.PositiveIntegerField(verbose_name='Год выпуска')
    description = models.TextField(verbose_name='Описание')
    # Здесь возможно стоит делать через отдельную модель через атрибут through
    # но это не точно =)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        blank=True,
        null=True,
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


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
        unique=True
    )

    # не уверена, что это нужно, но все же
    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']


class Comments(models.Model):
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
