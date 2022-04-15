from rest_framework import viewsets
from reviews.models import Review, Title
from .serializers import ReviewSerializer, CommentSerializer
from django.shortcuts import get_object_or_404


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        reviews = Review.objects.filter(
            title=get_object_or_404(Title, pk=title_id)
        )
        return reviews


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from reviews.models import Category, Genre, Review, Title

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    
