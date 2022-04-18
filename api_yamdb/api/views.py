import django_filters

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, views, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from reviews.models import Category, Genre, Title, User, Review, Comment
from .permissions import AdminOrReadOnly, AdminOnly


from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitlePostSerializer,
    NewUserSerializer,
    MyTokenObtainPairSerializer,
    ListUsersSerializer,
)


class MyTokenObtainPairView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, serializer):
        serializer = MyTokenObtainPairSerializer(data=serializer.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        # token = serializer.validated_data["confirmation_code"]
        # print(token)
        user = get_object_or_404(
            User, token=serializer.data["token"]
        )
        print(user)
        refresh = RefreshToken.for_user(user)
        result = {
            "token": str(refresh.access_token),
        }
        return Response(status=status.HTTP_200_OK, data=result)
    # def post(self, serializer):
    #     serializer = MyTokenObtainPairSerializer(data=serializer.data)
    #     serializer.is_valid(raise_exception=True)
    #     token = serializer.validated_data["token"]
    #     # user = get_object_or_404(User, token=token)
    #     username = serializer.validated_data["token"]
    #     print(username)
    #     if User.objects.filter(username=username).exists():
    #         refresh = RefreshToken.for_user(
    #             User.objects.filter(username=username)
    #         )
    #         result = {
    #             "token": str(refresh.access_token),
    #         }
    #         return Response(status=status.HTTP_200_OK, data=result)
    #     return Response(
    #         status=status.HTTP_404_NOT_FOUND, data=serializer.errors
    #     )
    # def post(self, serializer):
    #     serializer = MyTokenObtainPairSerializer(data=serializer.data)
    #     serializer.is_valid(raise_exception=True)
    #     # token = serializer.validated_data["token"]
    #     # user = get_object_or_404(User, token=token)
    #     print(serializer.data)
    #     username = serializer.validated_data["username"]
    #     if User.objects.filter(username=username).exists():
    #         refresh = RefreshToken.for_user(
    #             User.objects.filter(username=username)
    #         )
    #         result = {
    #             "token": str(refresh.access_token),
    #         }
    #         return Response(status=status.HTTP_200_OK, data=result)
    #     return Response(
    #         status=status.HTTP_404_NOT_FOUND, data=serializer.errors
    #     )
    # def post(self, serializer):
    #     serializer = MyTokenObtainPairSerializer(data=serializer.data)
    #     serializer.is_valid(raise_exception=True)
    #     # token = serializer.validated_data["token"]
    #     # user = get_object_or_404(User, token=token)
    #     username = serializer.data["username"]
    #     if User.objects.filter(username=username).exists():
    #         refresh = RefreshToken.for_user(
    #             User.objects.filter(username=username)
    #         )
    #         result = {
    #             "token": str(refresh.access_token),
    #         }
    #         return Response(status=status.HTTP_200_OK, data=result)
    #     return Response(
    #         status=status.HTTP_404_NOT_FOUND, data=serializer.errors
    #     )
    # def post(self, serializer):
    #     serializer = MyTokenObtainPairSerializer(data=serializer.data)
    #     serializer.is_valid(raise_exception=True)
    #     token = serializer.validated_data["token"]
    #     user = get_object_or_404(User, token=token)
    #     refresh = RefreshToken.for_user(user)
    #     result = {
    #         "token": str(refresh.access_token),
    #     }
    #     return Response(status=status.HTTP_200_OK, data=result)


class NewUserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """Регистрация нового пользователия.
    Отправка tokena на email пользователя."""

    queryset = User.objects.all()
    serializer_class = NewUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
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
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


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


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="slug")
    genre = django_filters.CharFilter(field_name="slug")

    class Meta:
        model = Title
        fields = ["category", "genre", "name", "year"]


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category", "genre", "name", "year")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleSerializer
        return TitlePostSerializer


class ListUsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ListUsersSerializer
    permission_classes = [
        IsAuthenticated,
        AdminOnly,
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        reviews = Review.objects.filter(
            title=get_object_or_404(Title, pk=title_id)
        )
        return reviews

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs.get("title_id"))


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_class = TitleFilter
