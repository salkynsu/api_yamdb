from rest_framework import serializers

from django.db.models import Sum

from reviews.models import Genre, Category, Title, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
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
        rating = reviews.aggregate(Sum('score')) / reviews.count()
        return rating
