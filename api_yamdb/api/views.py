from rest_framework import viewsets
from reviews.models import Review, Title
from .serializers import ReviewSerializer, CommentSerializer
from django.shortcuts import get_object_or_404


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        reviews = Review.objects.filter(
            title=get_object_or_404(Title, pk=title_id)
        )
        return reviews


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
