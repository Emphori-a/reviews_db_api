from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from reviews.models import Category, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer)
from .viewsets import CreateListDestroyViewSet
from .permissions import (IsAdminOrReadOnly,
                          IsModeratorIsAdminIsAuthorOrReadOnly)
from .filters import TitleFilterSet
from ..mixins import PutNotAllowed


class TitleViewSet(viewsets.ModelViewSet, PutNotAllowed):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-year')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet, PutNotAllowed):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsModeratorIsAdminIsAuthorOrReadOnly]

    def _get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self._get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self._get_title())


class CommentViewSet(viewsets.ModelViewSet, PutNotAllowed):
    serializer_class = CommentSerializer
    permission_classes = [
        IsModeratorIsAdminIsAuthorOrReadOnly]

    def _get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self._get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self._get_review())
