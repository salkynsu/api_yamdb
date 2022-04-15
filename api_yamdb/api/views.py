from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Genre, Category, Title, Review

from .serializers import GenreSerializer, CategorySerializer, TitleSerializer

from .permissions import AdminOrReadOnly


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly,]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly,]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    
