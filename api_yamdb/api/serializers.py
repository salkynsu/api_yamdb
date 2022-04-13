from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField
from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    title = PrimaryKeyRelatedField(read_only=True)
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ("id", "title", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    review = PrimaryKeyRelatedField(read_only=True)
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "review", "author", "pub_date")
