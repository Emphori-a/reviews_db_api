from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets

from reviews.models import Title
from .permissions import (IsAdminOrReadOnly,
                          IsModeratorIsAdminIsAuthorOrReadOnly)


class CreateListDestroyViewSet(
        mixins.CreateModelMixin, mixins.ListModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class ReviewCommentViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsModeratorIsAdminIsAuthorOrReadOnly]
    http_method_names = ('get', 'post', 'patch', 'delete')

    def _get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))
