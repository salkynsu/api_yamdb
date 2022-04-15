from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
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

urlpatterns = [
    path("v1/", include(router.urls)),
]
