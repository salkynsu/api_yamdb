from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    NewUserViewSet,
    MyTokenObtainPairView,
    ListUsersViewSet,
    UserMeAPIView,
    # UserMeUpdateAPIview,
)

app_name = "api"

router = SimpleRouter()
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("titles", TitleViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet, basename = "comments"
)
router.register("auth/signup", NewUserViewSet)
router.register("users", ListUsersViewSet)

urlpatterns = [
    path(
        "v1/auth/token/",
        MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("v1/users/me/", UserMeAPIView.as_view()),
    path("v1/", include(router.urls)),
]
