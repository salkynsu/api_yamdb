from django.db.models import Avg
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

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
    TokenObtainSerializer,
    NewUserSerializer,
    ReviewSerializer,
    TitlePostSerializer,
    TitleSerializer,
    UserDetailSerializer,
)


class TokenObtainView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(
                username=serializer.validated_data["username"]
            )
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.validated_data["token"] == user.token:
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
                get_object_or_404(
                    User, username=serializer.validated_data["username"]
                ).token
            ),
            settings.EMAIL_ADDRESS,
            [serializer.validated_data["email"]],
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

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="me",
        url_name="me",
    )
    def get_me(self, request):
        queryset = get_object_or_404(User, username=self.request.user)
        serializer = ListUsersSerializer(queryset)
        return Response(data=serializer.data)

    @action(
        detail=False,
        methods=["patch"],
        permission_classes=[IsAuthenticated, UserPermissions],
        url_path="me",
        url_name="me_patch",
    )
    def patch(self, request):
        queryset = get_object_or_404(User, username=self.request.user)
        serializer = UserDetailSerializer(
            queryset, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


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
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all().order_by("-pub_date")

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review_id=review_id)
