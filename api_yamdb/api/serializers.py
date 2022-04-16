from django.db.models import Sum
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from reviews.models import Category, Genre, Review, Title, User


class NewUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        write_only=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that email already exists.",
            )
        ],
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def create(self, validated_data):
        user = super(NewUserSerializer, self).create(validated_data)
        user.save()
        return user


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", many=False, queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "category",
            "genre",
        )

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj)
        rating = reviews.aggregate(Sum('score'))["score"] / reviews.count()
        return rating
