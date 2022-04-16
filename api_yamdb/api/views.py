from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny

from reviews.models import Category, Genre, Title, User

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    NewUserSerializer,
)

from .permissions import AdminOrReadOnly

class NewUserViewSet(
    CreateModelMixin, ListModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = NewUserSerializer
    permission_classes = [AllowAny]


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly,]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly,]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category", "genre", "name", "year")
