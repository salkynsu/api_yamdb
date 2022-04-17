from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, views
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status

from reviews.models import Category, Genre, Title, User

from .permissions import AdminOrReadOnly

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    NewUserSerializer,
    MyTokenObtainPairSerializer,
    ListUsersSeriaziler,
)


class MyTokenObtainPairView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, serializer):
        serializer = MyTokenObtainPairSerializer(data=serializer.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data["token"]
            user = get_object_or_404(User, token=token)
            refresh = RefreshToken.for_user(user)
            result = {
                "token": str(refresh.access_token),
            }
            return Response(status=status.HTTP_200_OK, data=result)
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
        )


class NewUserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """Регистрация нового пользователия.
    Отправка tokena на email пользователя."""

    queryset = User.objects.all()
    serializer_class = NewUserSerializer
    permission_classes = [AllowAny]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        send_mail(
            "Confirmation code here",
            "Here is the confirmation code: "
            + str(
                User.objects.get(username=serializer.data["username"]).token
            ),
            "admin@admin.com",
            [serializer.data["email"]],
            fail_silently=False,
        )


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


class ListUsersViesSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ListUsersSeriaziler
    permission_classes = [
        AdminOrReadOnly,
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
