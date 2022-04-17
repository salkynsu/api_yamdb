from django.db.models import Sum
from rest_framework import serializers, relations
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Review, Title, User


class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MyTokenObtainPairSerializer(serializers.ModelSerializer):
    username = relations.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = User
        fields = ("username", "token")

        # validators = [
        #    UniqueTogetherValidator(
        #        queryset=User.objects.all(), fields=["username", "token"]
        #    )
        # ]


class NewUserSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации нового пользователя."""

    class Meta:
        model = User
        fields = ("username", "email")

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError("Данное имя недопустимо!")
        return data


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
