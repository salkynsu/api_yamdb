from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenRefreshView,
    # TokenVerifyView,
)

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    NewUserViewSet
)

app_name = "api"

router = SimpleRouter()
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("titles", TitleViewSet)
router.register(r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
)
router.register("auth/signup/", NewUserViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"), ]
