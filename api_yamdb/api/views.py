from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from reviews.models import Category, Genre, Review, Title, Comment, User

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    NewUserSerializer,
)
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from .permissions import AdminOrReadOnly


class NewUserViewSet(
    CreateModelMixin, ListModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = NewUserSerializer
    permission_classes = [AllowAny]


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category", "genre", "name", "year")


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     title_id = self.kwargs.get("title_id")
    #     reviews = Review.objects.filter(
    #         title=get_object_or_404(Title, pk=title_id)
    #     )
    #     return reviews


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
