import binascii
import os

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    ROLE_CHOICE = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    )

    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=ROLE_CHOICE,
        default="user",
        max_length=50,
    )
    token = models.CharField(max_length=40)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="title"
    )
    genre = models.ManyToManyField(Genre, through="GenreTitle")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]


class GenreTitle(models.Model):
    """Модель связи многие-ко-многим произведения и жанра."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    """Модель отзыва к произведению."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="review"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review"
    )
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="author_review_title"
            )
        ]


class Comment(models.Model):
    """Модель комментария к отзыву."""

    text = models.TextField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comment"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment"
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
