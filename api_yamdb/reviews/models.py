from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 1
    MODERATOR = 2
    ADMIN = 3

    ROLE_CHOICE = ((USER, "User"), (MODERATOR, "Moderator"), (ADMIN, "Admin"))

    bio = models.TextField(blank=True)
    role = models.CharField(choices=ROLE_CHOICE, default=1, max_length=50)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
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
    pub_date = models.DateField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comment"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment"
    )
    pub_date = models.DateField(auto_now_add=True)
