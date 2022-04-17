from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    NewUserViewSet,
    MyTokenObtainPairView,
    ListUsersViesSet,
)

app_name = "api"

router = SimpleRouter()
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("titles", TitleViewSet)
router.register("auth/signup", NewUserViewSet)
router.register("users", ListUsersViesSet)


urlpatterns = [
    path("v1/", include(router.urls)),
    path(
        "v1/auth/token/",
        MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
]
