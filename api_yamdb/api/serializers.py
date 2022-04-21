import datetime

from django.shortcuts import get_object_or_404
from rest_framework import relations, serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class TokenObtainSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(source="token", required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


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
        exclude = ["id"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["id"]


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(required=True, many=True)
    category = CategorySerializer(required=True)
    rating = serializers.IntegerField()

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


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", many=False, queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "category",
            "genre",
        )

    def validate_year(self, value):
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError(
                "Год должен быть не больше текущего."
            )
        return value


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)


class ReviewSerializer(serializers.ModelSerializer):
    author = relations.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError(
                "Оценка должна быть числом от 1 до 10."
            )
        return value

    def validate(self, data):
        user = self.context["request"].user
        title_id = self.context["view"].kwargs["title_id"]
        if (
            Review.objects.filter(
                title=get_object_or_404(Title, pk=title_id), author=user
            ).exists()
            and self.instance is None
        ):
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв к этому произведению."
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    review = relations.PrimaryKeyRelatedField(read_only=True)
    author = relations.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "review", "author", "pub_date")
