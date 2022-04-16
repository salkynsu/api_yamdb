import binascii
import os

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    ROLE_CHOICE = (
        ("User", "User"),
        ("Moderator", "Moderator"),
        ("Admin", "Admin"),
    )

    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=ROLE_CHOICE,
        default="User",
        max_length=50,
    )
    token = models.CharField(max_length=40)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()


class Genre(models.Model):
    class Meta:
        ordering = ["-id"]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        ordering = ["-id"]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    class Meta:
        ordering = ["-id"]

    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="title"
    )
    genre = models.ManyToManyField(Genre)
    description = models.TextField(blank=True)


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="review"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review"
    )
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comment"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment"
    )
    pub_date = models.DateTimeField(auto_now_add=True)
