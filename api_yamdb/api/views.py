from django.db.models import Avg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, views, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import CreateListDestroyModelMixin
from .permissions import (
    AdminModeratorOrReadOnly,
    AdminOnly,
    AdminOrReadOnly,
    UserPermissions,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ListUsersSerializer,
    MyTokenObtainPairSerializer,
    NewUserSerializer,
    ReviewSerializer,
    TitlePostSerializer,
    TitleSerializer,
    UserDetailSerializer,
)


class MyTokenObtainPairView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, serializer):
        serializer = MyTokenObtainPairSerializer(data=serializer.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = User.objects.get(username=serializer.data["username"])
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            token = serializer.data["confirmation_code"]
            print(token)
            print(user.token)

            if serializer.data["confirmation_code"] == user.token:
                refresh = RefreshToken.for_user(user)
                result = {
                    "token": str(refresh.access_token),
                }
                return Response(status=status.HTTP_200_OK, data=result)
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer.errors
            )


class NewUserViewSet(CreateModelMixin, viewsets.GenericViewSet):
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


class ListUsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = ListUsersSerializer
    permission_classes = [IsAuthenticated, AdminOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"


class UserMeAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, UserPermissions]
    pagination_class = None

    def get_queryset(self):
        return get_object_or_404(User, username=self.request.user)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = ListUsersSerializer(queryset)
        return Response(data=serializer.data)

    def patch(self, request):
        queryset = self.get_queryset()
        serializer = UserDetailSerializer(
            queryset, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data="Неверные данные", status=status.HTTP_400_BAD_REQUEST
        )


class GenreViewSet(CreateListDestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Genre.objects.all().order_by("-id")
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CategoryViewSet(CreateListDestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Category.objects.all().order_by("-id")
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [
        AdminOrReadOnly,
    ]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg("reviews__score")).order_by(
            "-id"
        )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        AdminModeratorOrReadOnly,
    ]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all().order_by("-pub_date")

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        serializer.save(author=self.request.user, title_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        AdminModeratorOrReadOnly,
    ]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        comments = Comment.objects.filter(
            review=get_object_or_404(Review, pk=review_id)
        ).order_by("-pub_date")
        return comments

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review_id=review_id)
