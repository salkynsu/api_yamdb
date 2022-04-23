from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)


class CreateListDestroyModelMixin(
    CreateModelMixin, DestroyModelMixin, ListModelMixin
):
    pass


