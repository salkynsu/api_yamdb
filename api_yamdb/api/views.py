import django_filters
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, views, viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title, User

from .permissions import AdminOrReadOnly, AdminOnly, UserPermissions

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitlePostSerializer,
    NewUserSerializer,
    MyTokenObtainPairSerializer,
    ListUsersSerializer,
    UserMeSerializer,
)


class MyTokenObtainPairView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, serializer):
        # serializer = MyTokenObtainPairSerializer(data=serializer.data)
        # serializer.is_valid(raise_exception=True)
        # token = serializer.validated_data["token"]
        # user = get_object_or_404(User, token=token)
        # if user.exists():
        #    refresh = RefreshToken.for_user(
        #        User.objects.filter(username=username)
        #    )
        #    result = {
        #        "token": str(refresh.access_token),
        #    }
        #    return Response(status=status.HTTP_200_OK, data=result)
        # return Response(
        #    status=status.HTTP_404_NOT_FOUND, data=serializer.errors
        # )
        serializer = MyTokenObtainPairSerializer(data=serializer.data)
        serializer.is_valid(raise_exception=True)
        # token = serializer.validated_data["confirmation_code"]
        # print(token)
        user = get_object_or_404(User, username=serializer.data["username"])
        refresh = RefreshToken.for_user(user)
        result = {
            "token": str(refresh.access_token),
        }
        return Response(status=status.HTTP_200_OK, data=result)
        # return Response(
        #    status=status.HTTP_404_NOT_FOUND, data=serializer.errors
        # )


class NewUserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """Регистрация нового пользователя.
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


class GenreViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CategoryViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")
    genre = django_filters.CharFilter(field_name="genre__slug")
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name="year")

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
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleSerializer
        return TitlePostSerializer


class ListUsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ListUsersSerializer
    permission_classes = [IsAuthenticated, AdminOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"


# class UserMeViewsSet(viewsets.GenericViewSet):
#    serializer_class = UserMeSerializer
#    permission_classes = [IsAuthenticated, AdminOnly]
#    pagination_class = None
#
#    def get_queryset(self):
#        return User.objects.filter(username=self.request.user)


class UserMeViewsSet(viewsets.ModelViewSet):
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)
