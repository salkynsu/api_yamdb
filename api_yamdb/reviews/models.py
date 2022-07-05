import binascii
import os

from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import year_validator, score_validator

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"


class User(AbstractUser):
    ROLE_CHOICE = (
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    )

    email = models.EmailField(
        unique=True, verbose_name="Адрес электронной почты"
    )
    bio = models.TextField(blank=True, verbose_name="О себе")
    role = models.CharField(
        choices=ROLE_CHOICE, default=USER, max_length=50, verbose_name="Роль"
    )
    token = models.CharField(max_length=40, verbose_name="Токен")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()


class Genre(models.Model):
    name = models.CharField(
        max_length=200, db_index=True, verbose_name="Название"
    )
    slug = models.SlugField(unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Жанр произведения"
        verbose_name_plural = "Жанры произведения"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=200, db_index=True, verbose_name="Название"
    )
    slug = models.SlugField(unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Категория произведения"
        verbose_name_plural = "Категории произведения"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200, db_index=True, verbose_name="Название"
    )
    year = models.PositiveSmallIntegerField(
        validators=[year_validator], verbose_name="Год"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name="titles",
        verbose_name="Категория произведения",
    )
    genre = models.ManyToManyField(Genre, verbose_name="Жанр произведения")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Заголовок отзыва",
    )
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    score = models.PositiveSmallIntegerField(
        validators=[score_validator], verbose_name="Оценка"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )

    class Meta:
        verbose_name = "Отзыв на произведение"
        verbose_name_plural = "Отзывы на произведения"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="author_review_title"
            )
        ]

    def __str__(self):
        return self.title.name


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв, к которому публикуется комментарий",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий к отзыву"
        verbose_name_plural = "Комментарии к отзыву"
