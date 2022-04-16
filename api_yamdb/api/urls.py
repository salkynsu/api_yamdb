from django.urls import include, path
from rest_framework.routers import SimpleRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenRefreshView,
    # TokenVerifyView,
)

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    NewUserViewSet,
    # TokenObtainPairView,
    MyTokenObtainPairView,
)

app_name = "api"

router = SimpleRouter()
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("titles", TitleViewSet)
router.register("auth/signup", NewUserViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
    path(
        "v1/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    # path(
    #    "v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    # ),
    # path("v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
