from django.db.models import Sum
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    TokenObtainPairSerializer,
    TokenObtainSlidingSerializer,
)


from reviews.models import Category, Genre, Review, Title, User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # class Meta:
    #    model = User
    #    fields = ("email", "token")

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["confirmation code"] = user.token

        return token


class NewUserSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации нового пользоователя."""

    class Meta:
        model = User
        fields = ("username", "email")


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
